from flask import render_template, request,  redirect, session, flash, jsonify
import requests 
from main import app


# Rota para renderizar a página inicial do usuário
@app.route('/')
def index():
    return render_template('/index.html')
# Rota para renderizar a página de login
@app.route('/login')
def login():
    proxima = session.pop('next_page', '/inicial_gestao')
    return render_template('/login.html', proxima=proxima)

# Rota para autenticar o login
@app.route('/authenticate', methods=['POST'])
def authenticate_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        backend_url = "https://backend-oxelearning.deyvessoncarlos.repl.co/login"
        payload = {
            'user': email,
            'password': password
        }
        response = requests.post(backend_url, data=payload)
        
        if response.status_code == 200:
            print(response.json())
            user_data = response.json()['user']
            session['user_data'] = user_data
            proxima_pagina = request.form.get('proxima', '/')
            return redirect(proxima_pagina)
        elif response.status_code == 401:
            flash('Usuário ou Senha incorretos!')
            return redirect('/login')
        else: 
            flash('Erro no Servidor')
    
    
# Rota para renderizar a página inicial de gestão
@app.route('/inicial_gestao')
def index_gestao():
    if 'user_data' not in session or session['user_data'] is None:
        session['next_page'] = '/inicial_gestao'  # Armazena a próxima página antes de redirecionar para o login
        return redirect('/login')

    response = requests.get("https://backend-oxelearning.deyvessoncarlos.repl.co/getFiles")
    is_admin = session['user_data'].get('admin')
    print(is_admin)# Defina essa variável de acordo com a lógica de autenticação
    return render_template('/index_gestao.html', arquivos=response.json(), is_admin=is_admin)
    


@app.route('/redefinir_senha')
def redefinir_senha():
    return render_template('/redefinir_senha.html')

@app.route('/resetPassword', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    if email:
        backend_url = "https://backend-oxelearning.deyvessoncarlos.repl.co/resetPassword"
        payload = {
            'email': email
        }
        response = requests.post(backend_url, data=payload)
        if response.status_code == 200:
            flash("Foi enviado um link para restauração de senha no seu e-mail.")
            return redirect('/login')
        else: #response.status_code == 401:
            flash("Email não cadastrado!")
            return redirect('/recuperar')
            
    else:
        return jsonify({'error': 'O email não foi fornecido'}), 400
    

@app.route('/cadastrar')

def cadastrar():
    if 'user_data' not in session or session['user_data'] is None :
        session['next_page'] = '/inicial_gestao'  # Armazena a próxima página antes de redirecionar para o login
        return redirect('/login')
    if session['user_data'].get('admin') == False:
        print(session['user_data'].get('admin') )
        return redirect("/inicial_gestao")

    response = requests.get("https://backend-oxelearning.deyvessoncarlos.repl.co/getUsers")
    return render_template('/cadastrar.html', arquivos=response.json())


@app.route('/cadastro_user', methods=['POST'])
def cadastro_user():
    name = request.form.get('nomeUsuario')  # Update with correct field name
    email = request.form.get('emailUsuario')  # Update with correct field name
    password = request.form.get('senhaUsuario')  # Update with correct field name

    if email and password:
        backend_url = "https://backend-oxelearning.deyvessoncarlos.repl.co/signUp"
        payload = {
            'name': name,
            'user': email,
            'password': password
        }
        response = requests.post(backend_url, data=payload)
        if response.status_code == 201:
            flash('Gestor cadastrado com Sucesso!')
            return redirect('/cadastrar')
        elif response.status_code == 401:
            flash('Usuário Já cadastrado')
            return redirect('/cadastrar')
        else: 
            flash('Erro no Servidor')
            return redirect('/cadastrar')
        
            
    
@app.route('/deletarUser/<string:id>', methods=['GET', 'POST'])
def deletarUser(id):
    backend_delete_url = f"https://backend-oxelearning.deyvessoncarlos.repl.co/deleteUser"
    try:
        # Envia uma solicitação para a API externa para deletar o arquivo com o ID fornecido
        print(backend_delete_url)
        response_delete = requests.post(backend_delete_url, json={'userID': id})
        if response_delete.status_code == 200:
            flash("Usuario Excluido com Sucesso!")
            return redirect('/cadastrar')
        # Redireciona para a rota que lista os arquivos após a deleção    
        else:
            return "Erro ao deletar o arquivo na API externa."
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API: {e}"
    
# Rota para efetuar logout
@app.route('/logout')
def logout():
    print(session['user_data'])
    session['user_data'] = None
    # flash('Logout efetuado com Sucesso!')
    return redirect('/')