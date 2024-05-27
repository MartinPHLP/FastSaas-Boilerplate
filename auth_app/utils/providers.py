from google.auth.transport import requests
import requests

def get_google_user_info(token):
    response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}')
    if response.status_code == 200:
        data = response.json()
        user_id = data['user_id']
        email = data['email']
        response = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={token}')
        if response.status_code == 200:
            data = response.json()
            picture_url = data.get('picture')
            return user_id, email, picture_url
        else:
            raise ValueError('Invalid token ish')
    else:
        raise ValueError('Invalid token')
