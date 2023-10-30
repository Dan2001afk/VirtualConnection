from django.shortcuts import render, redirect
from firebase_admin import auth
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from firebase_admin import credentials
from .firebase_config import cred  # Ajusta la importación según la ubicación de tu archivo de configuración
import firebase_admin

# Asegúrate de que la aplicación se inicialice antes de realizar cualquier operación de Firebase
cred = credentials.Certificate("C:/Users/camilo/Desktop/VirtualConnection/VirtualConnection/AppVirtualConnection/virtualconnection-643e6-firebase-adminsdk-cb76t-6447f0115e.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/'
    })


def RegistroUsuarios(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            
            try:
                # Verificar si las contraseñas coinciden nuevamente
                if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
                    error_message = "Las contraseñas no coinciden"
                    return render(request, 'register.html', {'form': form, 'error_message': error_message})
                
                # Crear un nuevo usuario en Firebase
                user = auth.create_user(
                    email=email,
                    password=password,
                )
                
                # Puedes agregar el nombre de usuario como atributo personalizado en Firebase (opcional).
                auth.update_user(
                    user.uid,
                    display_name=username
                )

                # Redirigir al usuario a la página de bienvenida
                
                return render(request, 'Dashboard.html')

            except Exception as e:
                # Manejar errores, por ejemplo, si el usuario ya existe.
                error_message = str(e)
                return render(request, 'register.html', {'form': form, 'error_message': error_message})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
