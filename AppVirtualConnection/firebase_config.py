import firebase_admin
from firebase_admin import credentials

from firebase_admin import auth


# Inicializa la aplicación Firebase con las credenciales
cred = credentials.Certificate("C:/Users/camilo/Desktop/django oficial/VirtualConnection/AppVirtualConnection/virtualconnection-643e6-firebase-adminsdk-cb76t-6447f0115e.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/'
    })


