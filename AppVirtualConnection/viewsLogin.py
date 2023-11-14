#VISTAS PARA REGISTRO DE USUARIOS Y LOGEO
from .forms import *
from firebase_admin import credentials
from .firebase_config import cred #CONEXION Y LLAMADO DE LA BASE DE DATOS FIRABASE
from django.shortcuts import render, redirect
import json
import requests
from .forms import RegistroForm
from firebase_admin import auth
from django.http import JsonResponse

# Asegúrate de importar el formulario adecuado



def login_firebase(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # ENVIAMOS LA  SOLICITUT A LA API REST DE  FIREBASE PARA LOGUEAR EL USUARIO
        auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA"

        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(auth_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            user_data = response.json()
            #LAS CONDICIONES QUE ESTAN SE CUMPLEN SOLO SI LA SOLICITUD DA UN STATUS DE  200
            #PODEMOS HACER MUCHAS COSAS CON LA INFORMACION QUE SE RECIBE AL INICIAR SESION
            return redirect('EstadisticasPage')  #REDIRIGIMOS AL USUARIO DEPENDIENDO EL ROL
        else:
            # MENSAJES PARA CADA UNO DE LOS CASOS AL MOMENTO DE INICIAR SESION
            if error_message == "INVALID_PASSWORD":
                error_message = "Contraseña incorrecta"
            elif error_message == "EMAIL_NOT_FOUND":
                error_message = "Usuario no registrado"
            elif error_message == "USER_DISABLED":
                error_message = "Bloqueo de cuenta"
            else:
                error_message = "Error de autenticación"
    #RETORNAMOS AL LA VISTA DEL FORMULARIO Y MOSTRAMOS EL ERROR 
    return render(request, 'login.html', {'error_message': error_message})




def registro_usuario(request):
    if request.method == 'POST':
        #LLAMADO DEL FORMULARIO PARA REGISTRAR EL USUARIO
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # ENVIAMOS LA  SOLICITUT A LA API REST DE  FIREBASE PARA CREAR EL USUARIO NUEVO
            auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA"
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            response = requests.post(auth_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                #ESTAS VALIDACIONES SE CUMPLEN SI EL USUARIO SE REGISTRA CORRECTAMENTE Y TENEMOS UN STATUS DE 200
                return redirect('login')  # REDIRECCIONAMOS EL USUARIO A SU VISTA DENDIENDO EL ROL
            else:
                #SI AL REGISTRAR EL USUARIO HAY UN ERROR CON EL ERROR_MESSAGE LO MOSTRARA 
                #Y NOS REDIRRECCIONA AL FORMULARIO DE REGISTRO NUEVAMENTE
                error_message = response.json().get('error', {}).get('message', 'Error de registro')
                return render(request, 'register.html', {'error_message': error_message})

    else:
        form = RegistroForm()

    return render(request, 'register.html', {'form': form})





#recuperar contraseña

import requests

def reset_password_firebase(email):
    # Reemplaza 'API_KEY' con la clave de la API de tu proyecto Firebase
    api_key = 'AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA'
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'

    # Cuerpo de la solicitud para restablecer la contraseña
    data = {
        'requestType': 'PASSWORD_RESET',
        'email': email,
    }

    # Realiza la solicitud a la API REST de Firebase
    response = requests.post(url, json=data)

    # Procesa la respuesta
    if response.ok:
        print('Correo electrónico de restablecimiento de contraseña enviado con éxito')
    else:
        print(f'Error al enviar el correo electrónico de restablecimiento de contraseña: {response.text}')

# Ejemplo de uso
email = 'camolo.777@gmail.com'
reset_password_firebase(email)




def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Llama a la función para restablecer la contraseña en Firebase
        result = reset_password_firebase(email)

        # Maneja el caso en que la función devuelve None
        if result is None:
            return JsonResponse({'success': False, 'error_message': 'Hubo un error al procesar la solicitud.'})

        # Desempaqueta el resultado
        success, message = result

        # Devuelve una respuesta JSON
        if success:
            return JsonResponse({'success': True, 'message': message})
        else:
            return JsonResponse({'success': False, 'error_message': message})

    return render(request, 'reset_password.html')
