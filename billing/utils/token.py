import requests

def getAccessToken(url, client_id, secret):
    data = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers, auth=(client_id, secret))

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None
