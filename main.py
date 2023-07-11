from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from firebase import initialize_firebase
import requests
import json
import os

#Carregando as variáveis de ambiente
load_dotenv()

firebase = initialize_firebase()
auth = firebase.auth()

app = Flask(__name__)

@app.route('/')
def index():
  return jsonify({"response":"Backend Oxe Learning"}), 201

@app.route('/signUp', methods=['POST'])
def signup():
  if request.form.get('user') and request.form.get('password'):
    try:
      # Cria o usuário com email e senha
      user = auth.create_user_with_email_and_password(request.form.get('user'),request.form.get('password'))
      return jsonify({
        "message":"Login criado com sucesso",
        "user": user
      }), 201
    except Exception as e:
      error_data = json.loads(e.args[1])
      # Se o erro for de Usuário já existente
      if error_data['error']['message'] == 'EMAIL_EXISTS':
        return jsonify({
          "message":"Usuário já cadastrado"
        }), 400
      else:
        return jsonify({
          "message": f"Erro desconhecido: {e}"
        }), 500
  else:
    return jsonify({
      "message":"User ou Password não enviados"
    }), 400

@app.route('/login', methods=['POST'])
def login():
  if request.form.get('user') and request.form.get('password'):
    try:
      # Autentica o usuário com email e senha
      user = auth.sign_in_with_email_and_password(request.form.get('user'),request.form.get('password'))
      return jsonify({
        "message":"Usuário logado com sucesso",
        "user": user
      }), 200
    except Exception as e:
      error_data = json.loads(e.args[1])
      #Se o erro for de usuário ou senha incorretos
      if error_data['error']['message'] == 'EMAIL_NOT_FOUND' or error_data['error']['message'] == 'INVALID_PASSWORD':
        return jsonify({
          'message': 'Usuário ou Senha incorretos.'
        }), 401
      else:
        return jsonify({
          'message': f"Erro desconhecido: {e}"
        }), 500
  else:
    return jsonify({
      "message":"User ou Password não enviados"
    }), 400

@app.route('/uploadFile', methods=['POST'])
def upload_file():
  # Verifica se um arquivo foi enviado na requisição
  if 'file' not in request.files:
    return jsonify({"message":"Nenhum arquivo enviado"}), 400

  file = request.files['file']

  # Realiza o upload do arquivo para o ChatPDF
  files = [
    ('file', ('file', file, 'application/octet-stream'))
  ]
  headers = {
    'x-api-key': os.getenv('chatPDF_KEY')
  }

  response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files, verify=False)
  
  if response.status_code == 200:
    return jsonify({
      "message":"Arquivo enviado com sucesso",
      "sourceId": response.json()['sourceId']
    }), 201
  else:
    print('Status:', response.status_code)
    print('Error:', response.text)
    return jsonify({
      "message": f"Erro ao realizar o Upload do arquivo: {response.text}"
    }), 500

# Inicia a API
app.run(host='0.0.0.0', port=81)
