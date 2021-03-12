import json
import requests

        
MELI_API_URL = 'https://api.mercadolibre.com'

class MeliRest():
    
    def __init__(self, app_id, app_secret, 
                client_id, client_access_token,
                client_code, refresh_token, redirect_uri):
        self.app_id = app_id
        self.app_secret = app_secret
        self.client_id = client_id
        self.client_access_token = client_access_token
        self.client_code = client_code
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri


    def meli_url(self, path):
        return MELI_API_URL+path

    def profile(self):
        params = {'access_token': self.client_access_token}
        url = self.meli_url("/users/me")
        response = requests.get(url, params=params)
        return parse(response)

    def orders(self, last_date_closed, page=1):
        offset = (page - 1) * 50
        params = {'access_token': self.client_access_token, 
                    'seller': self.client_id,
                    'date.date_closed_from':  last_date_closed,
                    'sort': 'date_desc', 
                    'offset': offset}

        url = self.meli_url("/orders/search")
        response = requests.get(url, params=params)
        if response.ok:
            return json.loads(response.content.decode())['results']
        return []
        # si el token no esta ok va a devolver error
        

    def order(self, id):
        params = {'access_token': self.client_access_token}
        url = self.meli_url("/orders/{}".format(id))
        response = requests.get(url, params=params)
        if response.ok:
            return json.loads(response.content.decode())

    def shipping(self, id):
        params = {'access_token': self.client_access_token}
        url = self.meli_url("/shipments/{}".format(id))
        response = requests.get(url, params=params)
        if response.ok:
            return json.loads(response.content.decode())
        return {}

    def parse(self, response):
        return json.loads(response)

    def get_refresh_token(self):

        url = self.meli_url("/oauth/token?grant_type=refresh_token&client_id={}&client_secret={}&refresh_token={}"\
            .format(self.app_id, self.app_secret, self.refresh_token))
        response = requests.post(url)
        if response.ok:
            # actualizar access token, y refresh token en file y en clase
            self.client_access_token = json.loads(response.content.decode())['access_token']
            self.refresh_token = json.loads(response.content.decode())['refresh_token']
            return True
        return False
        # response = requests.post(url , params = {
        #     'client_id': self.app_id,
        #     'client_secret': self.app_secret,
        #     'code': self.client_code,
        #     'redirect_uri': 'https://luckymart.herokuapp.com'
        #     })


    def get_token(self):

        url = self.meli_url("/oauth/token?grant_type=authorization_code&client_id={}&client_secret={}&code={}&redirect_uri={}"\
                            .format(self.app_id, self.app_secret, self.client_code, self.redirect_uri))
        response = requests.post(url)
        if response.ok:
            # actualizar access token, y refresh token en file y en clase
            self.client_access_token = json.loads(response.content.decode())['access_token']
            self.refresh_token = json.loads(response.content.decode())['refresh_token']
            return True
        return False

        
        return response
