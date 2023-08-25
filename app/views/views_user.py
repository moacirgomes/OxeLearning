from flask import render_template, request,  redirect, session, flash
import requests 
from main import app


# Rota para renderizar a página inicial do usuário
@app.route('/inicial_user')
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
            user_data = response.json()['user']
            session['user_data'] = user_data
            proxima_pagina = request.form.get('proxima', '/')
            return redirect(proxima_pagina)
        else:
            flash('Usuário ou Senha incorretos!')
            return redirect('/login')
    
    
# Rota para renderizar a página inicial de gestão
@app.route('/inicial_gestao')
def index_gestao():
    if 'user_data' not in session or session['user_data'] is None:
        session['next_page'] = '/inicial_gestao'  # Armazena a próxima página antes de redirecionar para o login
        return redirect('/login')
    response = requests.get("https://backend-oxelearning.deyvessoncarlos.repl.co/getFiles")
    return render_template('/index_gestao.html', arquivos=response.json())

# Rota para efetuar logout
@app.route('/logout')
def logout():
    session['user_data'] = None
    # flash('Logout efetuado com Sucesso!')
    return redirect('/inicial_user')