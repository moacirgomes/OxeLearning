import json, os, requests
from flask import jsonify, request
from models.firebase import initialize_firebase
from models.firebaseSDK import delete_user_authentication

#iniciando conexão com o firebase
firebase = initialize_firebase()
auth = firebase.auth()
db = firebase.database()


def login():
  if request.form.get('user') and request.form.get('password'):
    try:
      # Autentica o usuário com email e senha
      user = auth.sign_in_with_email_and_password(request.form.get('user'),
                                                  request.form.get('password'))
      #Obtendo dados do usuário no banco do firebase
      firebase_iten = db.child("users").order_by_child("user").equal_to(request.form.get('user')).get()
      user['admin'] = firebase_iten[0].val()['admin']
      return jsonify({
        "message": "Usuário logado com sucesso",
        "user": user
      }), 200
    except Exception as e:
      error_data = json.loads(e.args[1])
      #Se o erro for de usuário ou senha incorretos
      if error_data['error']['message'] == 'EMAIL_NOT_FOUND' or error_data[
          'error']['message'] == 'INVALID_PASSWORD':
        return jsonify({'message': 'Usuário ou Senha incorretos.'}), 401
      else:
        return jsonify({'message': f"Erro desconhecido: {e}"}), 500
  else:
    return jsonify({"message": "User ou Password não enviados"}), 400


def signup():
  if request.form.get('user') and request.form.get(
      'password') and request.form.get('name'):
    try:
      # Cria o usuário com email e senha
      user = auth.create_user_with_email_and_password(
        request.form.get('user'), request.form.get('password'))
      db.child("users").push({
        "userID": user['localId'],
        "name": request.form.get('name'),
        "user": request.form.get('user'),
        "admin": False
      })
      return jsonify({
        "message": "Login criado com sucesso",
        "user": user
      }), 201
    except Exception as e:
      error_data = json.loads(e.args[1])
      # Se o erro for de Usuário já existente
      if error_data['error']['message'] == 'EMAIL_EXISTS':
        return jsonify({"message": "Usuário já cadastrado"}), 400
      else:
        return jsonify({"message": f"Erro desconhecido: {e}"}), 500
  else:
    return jsonify({"message": "User ou Password não enviados"}), 400


def reset_password():
  if request.form.get('email'):
    try:
      email = auth.send_password_reset_email(request.form.get('email'))
      return jsonify({
        "message": "Email enviado com sucesso!",
        "email": email
      }), 200
    except Exception as e:
      error_data = json.loads(e.args[1])
      #Se o erro for de usuário ou senha incorretos
      if error_data['error']['message'] == 'EMAIL_NOT_FOUND':
        return jsonify({'message': 'Email não cadastrado!'}), 401
      else:
        return jsonify({'message': f"Erro desconhecido: {e}"}), 500


def change_password():
  data = request.get_json()

  apiKey = os.environ['API_KEY']
  idToken = data.get('token')
  newPassword = data.get('new_password')

  url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={apiKey}"
  headers = {'Content-Type': 'application/json'}

  payload = {"idToken": idToken, "password": newPassword}
  response = requests.post(url, headers=headers, json=payload)

  if response.status_code == 200:
    return jsonify({
      "message": "Senha atualizada com sucesso!",
      "response": response.json()
    }), 200
  else:
    return jsonify({
      "message": "Erro ao alterar senha",
      "response": response.json()
    }), 500


def list_users():
  try:
    users = db.child("users").get()
    if users.val() == None or users.val() == "":
      #print(files.val())
      return jsonify({"message": "Nenhum arquivo cadastrado"}), 404

    array_users = []
    for user in users.each():
      array_users.append(user.val())
    return jsonify({
      "message": "lista de usuários obtida",
      "files": array_users
    }), 200
  except Exception as e:
    return jsonify({'message': f"Erro ao obter lista de usuários: {e}"}), 500


def delete_user():
  try:
    data = request.get_json()
    if (data.get('userID')):
      #Deletar User no Firebase Authentication
      delete_user_authentication(data.get('userID'))

      #Obtendo identificador do registro no Firebase Database
      firebase_iten = db.child("users").order_by_child("userID").equal_to(
        data.get('userID')).get()
      #Deletando registro no Firebase Database
      db.child("users").child(firebase_iten[0].key()).remove()
      return jsonify({
        "message": "Usuário removido com sucesso",
        "userID": data.get('userID')
      }), 200
    else:
      return jsonify({"message": "userID não enviado"}), 400
  except Exception as e:
    return jsonify({'message': f"Erro ao remover Usuário: {e}"}), 500
