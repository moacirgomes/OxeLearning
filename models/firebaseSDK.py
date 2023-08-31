import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("./models/oxelearning-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

def delete_user_authentication(uid):
  response = auth.delete_user(uid)
  return response
  