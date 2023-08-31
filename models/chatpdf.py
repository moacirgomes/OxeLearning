import os
import requests

#Função responsável por fazer a requisição que faz o Upload dos arquivos para o Chat PDF
def upload_file_chatpdf(files):
  
  #Montar Header da Requisição
  headers = {
    'x-api-key': os.environ['CHATPDF_KEY']
  }

  #Requisição para Upload do Arquivo no Chat PDF
  response = requests.post('https://api.chatpdf.com/v1/sources/add-file',
                           headers=headers,
                           files=files,
                          timeout=3000)

  return response

#Função responsável por fazer a requisição que obtem a resposta para a mensagem enviada
def get_response_chatpdf(sourceId, message, assistant):

  #Montar Header da Requisição
  headers = {
    "x-api-key": os.environ['CHATPDF_KEY'],
    "Content-Type": "application/json",
  }

  #Montar o Body da requisição
  data = {
    "sourceId": sourceId,
    "messages": [
      {
        "role": "assistant",
        "content": assistant
      },
      {
        "role": "user",
        "content": message,
      }
    ]
  }

  #Requisição para obter resposta do Chat PDF
  response = requests.post('https://api.chatpdf.com/v1/chats/message',
                             headers=headers,
                             json=data)

  return response
  