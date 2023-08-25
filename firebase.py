import pyrebase
import os
from dotenv import load_dotenv

#Carregando as variáveis de ambiente
load_dotenv()

def initialize_firebase():
    firebaseConfig = {
    "apiKey": os.getenv('apiKey'),
    "authDomain": os.getenv('authDomain'),
    "projectId": os.getenv('projectId'),
    "storageBucket": os.getenv('storageBucket'),
    "messagingSenderId": os.getenv('messagingSenderId'),
    "appId": os.getenv('appId'),
    "databaseURL": os.getenv('databaseURL')
    };

    return pyrebase.initialize_app(firebaseConfig)
