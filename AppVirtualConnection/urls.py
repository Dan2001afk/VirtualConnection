from django.urls import path
from .views import *
urlpatterns=[
        path('',Inicio,name="InicioPage"),
        path('Inicio',Inicio,name="InicioPage"),
        path('Dashboard/',Dashboard,name="DashboardPage"),
        path('Dispositivos/',Dispositivos,name="DispositivosPage"),
        path('Estadisticas/',Estadisticas,name="EstadisticasPage"),
        path('Alarmas/',Alarmas,name="AlarmasPage"),
        path('Tableros/',Tableros,name="TablerosPage"),
        path('Productos/',Productos,name="ProductosPage"),
        path('CerrarSesion/',CerrarSesion,name="CerrarSesionPage"),
]