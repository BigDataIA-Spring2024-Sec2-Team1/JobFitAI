import requests

def getAccessToken():
    url = "https://auth.emsicloud.com/connect/token"
    payload = "client_id=4v22ofaxe2m1np9c&client_secret=JAjNxQy0&grant_type=client_credentials&scope=emsi_open"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text
