from os.path import join
from typing import Any
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from bokeh.document import Document
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.themes import Theme
from .shape_viewer import shape_viewer
import matplotlib.pyplot as plt
from django.shortcuts import render


#Plantilla de inicio
def Inicio(request):
    return render (request, "Inicio.html")

#plantillas para usuario logueado

def Alarmas(request):
    return render (request, "Alarmas.html")

def Tableros(request):
    return render (request, "Tableros.html")

def Productos(request):
    return render (request, "Productos.html")

def Dispositivos(request):
    return render(request, 'Dispositivos.html')

def Estadisticas(request):
    return render(request, 'Estadisticas.html')

# plantilla para cerrar sesion
def CerrarSesion(request):
    return render (request, "CerrarSesion.html")


#pruebas django bockends

#Carga el archivo de configuracion theme.yaml creando un objeto teme y pasado a los graficos bokeh
theme = Theme(filename=join(settings.THEMES_DIR, "theme.yaml"))

#renderiza un template sin pasar datos adicionales
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {})


def shape_viewer_handler(doc: Document) -> None:
    panel = shape_viewer()
    panel.server_doc(doc)


def sea_surface_handler(doc: Document) -> None:
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type="datetime", y_range=(0, 25), y_axis_label="Temperature (Celsius)",
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line("time", "temperature", source=source)

    def callback(attr: str, old: Any, new: Any) -> None:
        if new == 0:
            data = df
        else:
            data = df.rolling(f"{new}D").mean()
        source.data = dict(ColumnDataSource(data=data).data)

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change("value", callback)

    doc.theme = theme
    doc.add_root(column(slider, plot))


def with_request(f):
    def wrapper(doc):
        return f(doc, doc.session_context.request)
    return wrapper


@with_request
def sea_surface_handler_with_template(doc: Document, request: Any) -> None:
    sea_surface_handler(doc)
    doc.template = """
{% block title %}Embedding a Bokeh Apps In Django{% endblock %}
{% block preamble %}
<style>
.bold { font-weight: bold; }
</style>
{% endblock %}
{% block contents %}
    <div>
    This Bokeh app below is served by a <span class="bold">Django</span> server for {{ username }}:
    </div>
    {{ super() }}
{% endblock %}
    """
    doc.template_variables["username"] = request.user


def sea_surface(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "embed.html", dict(script=script))


def sea_surface_custom_uri(request: HttpRequest) -> HttpResponse:
    script = server_document(request._current_scheme_host + "/sea_surface_custom_uri")
    return render(request, "embed.html", dict(script=script))


def shapes(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "embed.html", dict(script=script))

#prueba cuadricula

# myapp/views.py

from django.shortcuts import render
import panel as pn
from  .panel_app import create_panel_app

def panel_view(request):
    panel_app = create_panel_app()
    # # Servir la aplicación
    server = pn.serve(panel_app, show=False)
    # # Obtener el script y el div del layout
    script, div = pn.pane.HTML(panel_app).get_standalone()
    # # Detener el servidor
    server.stop()
    context = {"script": script, "div": div}
    #return render(request, "panel_template.html")
    return render(request, "panel_template.html", context)

from django.http import JsonResponse

import panel as pn
from .panel_app import create_panel_app

def dashboard(request):
    # panel_app = create_panel_app()

    # # Servir la aplicación
    # server = pn.serve(panel_app, show=False)

    # # Obtener el script y el div del layout
    # script, div = pn.pane.HTML(panel_app).get_standalone()

    # # Detener el servidor
    # server.stop()

    # context = {"script": script, "div": div}

    # if request.is_ajax():
    #     return JsonResponse(context)
    # else:
        return render(request, "dashboard.html")


from typing import List, Tuple

import numpy as np
import panel as pn

from awesome_panel import config

STYLE = """
.pn-stats-card div {
  line-height: 1em;
}
"""

ACCENT = config.ACCENT
OK_COLOR = config.PALETTE[2]
ERROR_COLOR = config.PALETTE[3]

HEADER = [config.get_header()]
app_html = 'pruebados.html' # Deberías reemplazar '...' con el valor correcto para 'app_html'
SIDEBAR_FOOTER = config.menu_fast_html(app_html=app_html, accent=ACCENT.encode)

if not STYLE in pn.config.raw_css:
    pn.config.raw_css.append(STYLE)


def _increment(value):
    draw = np.random.normal(1, 0.1, 1)[0]
    value *= draw
    value = max(0, value)
    value = min(100, value)
    return int(value)


def _create_callback(cards):
    async def update_card():
        for card in cards:
            card.value = _increment(card.value)

    return update_card


def AppIndicadores(intro_section, sidebar_footer) -> pn.template.FastGridTemplate:
    """Returns an app"""
    template = pn.template.FastGridTemplate(
        title="Streaming Indicators",
        row_height=140,
        accent_base_color=ACCENT,
        header_background=ACCENT,
        prevent_collision=True,
        save_layout=True,
        sidebar_footer=sidebar_footer,
        header=HEADER,
    )
    template.main[0:3, :] = intro_section

    indicators = []
    for row in range(0, 3):
        for col in range(0, 6):
            colors: List[Tuple[float, str]] = [(66, OK_COLOR), (100, ERROR_COLOR)]
            title = "Sensor " + str(row * 6 + col + 1)
            indicator = pn.indicators.Number(
                name=title,
                value=65,
                format="{value}%",
                colors=colors,
                css_classes=["pn-stats-card"],
            )
            template.main[row + 3, 2 * col : 2 * col + 2] = indicator
            indicators.append(indicator)

    for row in range(3, 5):
        for col in range(0, 3):
            title = "Sensor " + str(3 * row + col + 10)
            colors = [(0.7, OK_COLOR), (1, ERROR_COLOR)]
            indicator = pn.indicators.Gauge(
                name=title, value=65, bounds=(0, 100), colors=colors, align="center"
            )
            template.main[2 * row : 2 * row + 2, 4 * col : 4 * col + 4] = pn.Row(
                pn.layout.HSpacer(),
                indicator,
                pn.layout.HSpacer(),
            )
            indicators.append(indicator)

    # Create callback for all indicators
    return template


def serve():
    """Serves the app"""
    app = config.extension(url="streaming_indicators", template=None, intro_section=None)
    intro_section = app.intro_section()
    AppIndicadores(intro_section, SIDEBAR_FOOTER).servable()

    # Guardar la aplicación en un archivo HTML
    pn.panel(AppIndicadores(intro_section, SIDEBAR_FOOTER)).save(filename="panel_app.html", embed=True)

if __name__.startswith("bokeh"):
    serve()


def panel_view1(request):
    intro_section = None  # Puedes personalizar esto según tus necesidades
    sidebar_footer = None  # Puedes personalizar esto según tus necesidades
    app = AppIndicadores(intro_section, sidebar_footer)
    html = app.show(port=0, threaded=True)
    return render(request, 'pruebados.html', {'panel_html': html})


