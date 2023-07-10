from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

@app.route('/')
def index():
  return make_response(jsonify({"response":"Backend Oxe Learning"}),201)

@app.route('/uploadFile', methods=['POST'])
def upload_file():
  # Verifica se um arquivo foi enviado na requisição
  print(request.files)
  if 'file' not in request.files:
    return make_response(jsonify({"response":"Nenhum arquivo enviado"}),400)

  file = request.files['file']

  # Verifica se o arquivo possui um nome
  if file.filename == '':
    return make_response(jsonify({"response":"Nome do arquivo não encontrado"}),400)

  # Realiza o upload do arquivo para o ChatPDF
  #file.save(file.filename)
  files = [
    ('file', ('file', file, 'application/octet-stream'))
  ]
  print(files)
  headers = {
    'x-api-key': 'sec_1FGUxDVYQ6SeIoeBrqi1jUwLMXtbZzMi'
  }

  response = requests.post(
      'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
  
  if response.status_code == 200:
    print('Source ID:', response.json()['sourceId'])
    return make_response(jsonify({
      "response":"Arquivo enviado com sucesso!",
      "sourceId": response.json()['sourceId']
    }), 201)
  else:
    print('Status:', response.status_code)
    print('Error:', response.text)
    return make_response(jsonify({
      "response":"Erro ao realizar o Upload do arquivo."
    }), 500)

app.run(host='0.0.0.0', port=81)
