from flask import request, redirect, flash
import requests 
import os
import json
from main import app


# Rota para processar a pesquisa do usuário
@app.route('/pesquisar', methods=['POST'])
def pesquisar():
    retorno = ""
    data = request.get_json() 
    responseLista = requests.get("https://backend-oxelearning.deyvessoncarlos.repl.co/getFiles")
    if responseLista.status_code == 200: 
        # Itera sobre os arquivos disponíveis e envia a pergunta para cada um
        for item in responseLista.json()["files"]:
            headers = {'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding': 'gzip, deflate, br'} 
            dados = {'sourceId': f"{item['sourceID']}", 'message': data.get('pesquisa'), 'assistent': 'você faz parte da administração da faculdade e esta respondendo a um aluno, na resposta não precisa trazer o número da página e ignore também as respostas anteriores'}
            endpoint_url = "https://backend-oxelearning.deyvessoncarlos.repl.co/chatMessage"
            response = requests.post(endpoint_url, json=dados, headers=headers)
            response.content.decode('utf-8')
           
            retorno = response.json()["response"]
            break
        return retorno    
    else:
        return "Desculpe, não foi possível encontrar algo referente à sua pergunta!"



# Rota para cadastrar um novo arquivo
@app.route('/cadastro_arquivo', methods=['POST'])
def cadastro():
    if 'file' not in request.files:
        flash('No file part')
        
    file = request.files['file']
     
    if file.filename == '':
        flash('No selected file') 
    nome = request.form.get('nomeArquivo')
    validarTipoArquivo(file.filename)
    if nome and file and file.filename.endswith('.pdf'):
           
            print(file.filename)
            file.save('uploads/' + file.filename)
            files = {
                'file': (file.filename, open(f"uploads/{file.filename}", 'rb'), 'application/pdf'),
            }
            backend_url = "https://backend-oxelearning.deyvessoncarlos.repl.co/uploadFile"
            payload = {
                'name': nome
            }
            response = requests.post(backend_url, files=files, data=payload)
            files.clear()
            if response.status_code == 201:
                flash("PDF cadastrado com sucesso!")
                responseLista = requests.get("https://backend-oxelearning.deyvessoncarlos.repl.co/getFiles")
                salvarId = responseLista.json()["files"][-1]["sourceID"]      
                os.rename(r'uploads/'+file.filename, r"uploads/" + salvarId + ".pdf" )
             
    return redirect('/inicial_gestao')

# Rota para deletar um arquivo com o ID especificado
@app.route('/deletar/<string:id>', methods=['GET', 'POST'])
def deletar(id):
    backend_delete_url = f"https://backend-oxelearning.deyvessoncarlos.repl.co/deleteFile"
    try:
        # Envia uma solicitação para a API externa para deletar o arquivo com o ID fornecido
        response_delete = requests.post(backend_delete_url, json={'sourceID': id})
        if response_delete.status_code == 200:
            removeArquivo(id)
            return redirect('/inicial_gestao') # Redireciona para a rota que lista os arquivos após a deleção    
        else:
            return "Erro ao deletar o arquivo na API externa."
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API: {e}"

def removeArquivo(id):
        caminho_arquivo = os.path.join("uploads", f"{id}.pdf") 
        if caminho_arquivo:
                flash("Arquivo Removido com Sucesso!")
                os.remove(caminho_arquivo)  # Remove o arquivo localmente
        flash('Arquivo não encontrado na base de dados!')  
       
             
def validarTipoArquivo(file):
    novoFile = file.split('.')
    print(novoFile)
    if novoFile[1].lower() != "pdf":
        flash('Selecione um Arquivo do Tipo PDF!')
    return redirect('/inicial_gestao')

