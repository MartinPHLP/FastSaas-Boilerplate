from google.auth.transport import requests
from google.oauth2 import id_token
import os

def GetGoogleUserInfo(token):
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
    userid = idinfo['sub']
    email = idinfo.get('email')
    return userid, email
