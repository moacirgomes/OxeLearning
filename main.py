from flask import Flask, jsonify

from controllers.user_controller import login, signup, reset_password, change_password, list_users, delete_user
from controllers.chatpdf_controller import upload_file, chat_message, list_files, delete_file, update_file, clean_lista

app = Flask(__name__)


@app.route('/')
def index():
  return jsonify({"response": "Backend Oxe Learning UP!"}), 200


# Rota de Cadastro de usuário
app.add_url_rule('/signUp', 'signup', signup, methods=['POST'])

# Rota de Login
app.add_url_rule('/login', 'login', login, methods=['POST'])

# Rota para Redefinir Senha
app.add_url_rule('/resetPassword',
                 'resetPassword',
                 reset_password,
                 methods=['POST'])

# Rota para alterar Senha
app.add_url_rule('/changePassword',
                 'changePassword',
                 change_password,
                 methods=['POST'])

# Endpoint para obter lista de usuários
app.add_url_rule('/getUsers', 'getUsers', list_users, methods=['GET'])

# Endpoint para remover Usuário
app.add_url_rule('/deleteUser', 'deleteUser', delete_user, methods=['POST'])

# Endpoint para upload de arquivos
app.add_url_rule('/uploadFile', 'uploadFile', upload_file, methods=['POST'])

# Endpoint para obter lista de arquivos
app.add_url_rule('/getFiles', 'getFiles', list_files, methods=['GET'])

# Endpoint para remover arquivo
app.add_url_rule('/deleteFile', 'deleteFile', delete_file, methods=['POST'])

# Endpoint para atualizar arquivo
app.add_url_rule('/updateFile', 'updateFile', update_file, methods=['PUT'])

app.add_url_rule('/cleanLista', 'cleanLista', clean_lista, methods=['DELETE'])

# Endpoint para Enviar perguntas
app.add_url_rule('/chatMessage', 'chatMessage', chat_message, methods=['POST'])

# Inicia a API
app.run(host='0.0.0.0')
