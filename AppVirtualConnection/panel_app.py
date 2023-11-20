import hvplot.pandas
import numpy as np
import panel as pn
import pandas as pd

# def create_panel_app():
#     xs = np.linspace(0, np.pi)
#     pn.config.theme = 'dark'

#     freq = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
#     phase = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)

#     def sine(freq, phase):
#         return pd.DataFrame(dict(y=np.sin(xs*freq+phase)), index=xs)

#     def cosine(freq, phase):
#         return pd.DataFrame(dict(y=np.cos(xs*freq+phase)), index=xs)

#     dfi_sine = hvplot.bind(sine, freq, phase).interactive()
#     dfi_cosine = hvplot.bind(cosine, freq, phase).interactive()

#     plot_opts = dict(
#         responsive=True, min_height=400,
#         color=pn.template.FastGridTemplate.accent_base_color
#     )

#     template = pn.template.FastGridTemplate(
#         title="FastGridTemplate",
#         sidebar=[freq, phase],
#     )

#     template.main[:3, :6] = dfi_sine.hvplot(title='Sine', **plot_opts).output()
#     template.main[:3, 6:] = dfi_cosine.hvplot(title='Cosine', **plot_opts).output()

import hvplot.pandas
import numpy as np
import panel as pn
import pandas as pd
from bokeh.io import curdoc


def create_panel_app():
    pn.config.theme = 'default'

    # Datos y funciones para las gráficas
    xs = np.linspace(0, np.pi)

    def sine(freq, phase):
        return pd.DataFrame(dict(y=np.sin(xs*freq+phase)), index=xs)

    def cosine(freq, phase):
        return pd.DataFrame(dict(y=np.cos(xs*freq+phase)), index=xs)

    # Configuración de la cuadrícula
    grid_template = pn.template.FastGridTemplate(
        title="Grid Template Example",
        theme="dark",
        main_layout="card",  # Wrap main components in a card
        row_height=150,
        prevent_collision=True,
        save_layout=True
    )

    # Sliders para controlar las funciones
    freq_slider = pn.widgets.FloatSlider(name="Frequency", start=0, end=10, value=2)
    phase_slider = pn.widgets.FloatSlider(name="Phase", start=0, end=np.pi)

    # Funciones interacticas
    dfi_sine = hvplot.bind(sine, freq_slider, phase_slider).interactive()
    dfi_cosine = hvplot.bind(cosine, freq_slider, phase_slider).interactive()

    # Agregar las gráficas a la cuadrícula
    grid_template.main[0:6, 0:6] = dfi_sine.hvplot(title='Sine')
    grid_template.main[0:6, 6:] = dfi_cosine.hvplot(title='Cosine')

    return grid_template

if __name__ == "__main__":
    app = create_panel_app()
    app.servable()

    # Ejecutar la aplicación en el puerto 8080
    
