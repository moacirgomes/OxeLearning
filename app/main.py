from flask import Flask
'''
class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.sennha = senha '''

app = Flask(__name__)
app.config.from_pyfile('config.py')

from views.views_chat_pdf import *
from  views.views_user import *

if __name__ == '__main__':
     app.run(debug=True)
