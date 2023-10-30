import firebase_admin
from firebase_admin import credentials

from firebase_admin import auth


# Inicializa la aplicación Firebase con las credenciales
cred = credentials.Certificate("C:/Users/camilo/Desktop/VirtualConnection/VirtualConnection/AppVirtualConnection/virtualconnection-643e6-firebase-adminsdk-cb76t-6447f0115e.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/'
})


