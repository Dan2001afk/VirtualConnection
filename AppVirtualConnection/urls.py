from django.urls import path

from .views import *
from .viewsLogin import *
from django.urls import path
from . import views
from . import viewsLogin


urlpatterns=[
        
        path('In',Inicio,name="InicioPage"),
        path('Inicio',Inicio,name="InicioPage"),
        path('Dashboard/',dashboard,name="DashboardPage"),
        path('Dispositivos/',Dispositivos,name="DispositivosPage"),
        path('Estadisticas/',Estadisticas,name="EstadisticasPage"),
        path('Alarmas/',Alarmas,name="AlarmasPage"),
        path('Tableros/',Tableros,name="TablerosPage"),
        path('Productos/',Productos,name="ProductosPage"),


        #Autenticacion
        path('IniciarSesion/', viewsLogin.login_firebase, name='login'),
        path('RegistrarUsuarios/', viewsLogin.registro_usuario, name='Registro'),
        
        #recuperacion de contraseña
        path('reset-password/', reset_password_view, name='Reset-passwordPage'),
        
        #panel 
        path('panel/', panel_view, name='panel'),
        path('paneldos/', panel_view1, name='panel1'),
        

        

]       