from django.shortcuts import render


#renderizado de las plantillas
def Inicio(request):
    return render (request, "Inicio.html")

#plantillas logueado
def Dashboard(request):
    return render (request, "Dashboard.html")


def Alarmas(request):
    return render (request, "Alarmas.html")

def Tableros(request):
    return render (request, "Tableros.html")

def Productos(request):
    return render (request, "Productos.html")

#logout
def CerrarSesion(request):
    return render (request, "CerrarSesion.html")




#graficos libreria plotly
import plotly.express as px
from django.shortcuts import render

def Dispositivos(request):

    data = {'Categoría': ['A', 'B', 'C', 'D'], 'Valores': [1, 2, 3, 4]}
    fig = px.bar(data, x='Categoría', y='Valores', title='Ejemplo de gráfico de barras')
    div = fig.to_html(full_html=False)

    return render(request, 'Dispositivos.html', {'graph': div})


#graficos matplotlib plotly

import matplotlib.pyplot as plt
from django.shortcuts import render
from .forms import GraficaForm
from io import BytesIO
import base64


def Estadisticas(request):
    if request.method == 'POST':
        form = GraficaForm(request.POST)
        if form.is_valid():
            dato_x = form.cleaned_data['dato_x']
            dato_y = form.cleaned_data['dato_y']

            # Convierte los datos en listas de números (asegúrate de manejar errores)
            datos_x = [float(x) for x in dato_x.split(",")]
            datos_y = [float(y) for y in dato_y.split(",")]

            # Crea la gráfica
            plt.plot(datos_x, datos_y)
            plt.xlabel("Eje X")
            plt.ylabel("Eje Y")
            plt.title("Mi Gráfica")

            # Convierte la gráfica en un formato de imagen
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            # Convierte la imagen en formato base64
            image_base64 = base64.b64encode(buffer.read()).decode()

            return render(request, 'Estadisticas.html', {'form': form, 'imagen_grafica': image_base64})
    else:
        form = GraficaForm()
    return render(request, 'Estadisticas.html', {'form': form})





# sliders_app/views.py

from django.shortcuts import render
from .pn_app import create_sine_wave_app

def Dispositivos(request):
    sine_wave_app = create_sine_wave_app()  # Crea la aplicación Panel
    componente_sine_wave = sine_wave_app  # Suponiendo que el componente se encuentra directamente en la aplicación
    componente_sine_wave_str = componente_sine_wave.pprint()
    return render(request, 'Dispositivos.html', {'componente_sine_wave_str': componente_sine_wave_str})