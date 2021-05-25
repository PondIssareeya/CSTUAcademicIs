import json
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

ICT_AUTH_URL = "https://restapi.tu.ac.th/api/v1/auth/Ad/verify"
class ICT_Backend:
    """Authenticate using TU's ICT web service
    """
    def check_password(self, username, password):
        headers = {
            'Content-Type': 'application/json',
            'Application-Key' : settings.ICT_AUTH_APP_KEY
        }
        data = {'UserName': username, 'PassWord': password}
        try:
            result = requests.post(ICT_AUTH_URL, data=json.dumps(data), headers=headers)
            resp = result.json()
            return resp['status'] == True
        except Exception as e:
            print(str(e))
        return False

    def authenticate(self,request, username=None, password=None):
        
        try:
            user = User.objects.get(username=username)
            
        except User.DoesNotExist:
            # Since user has to be added to section before using
            # any functionality, we do not create new user on
            # the fly
            print("user doesn't exist in local table")
            return None 

        if self.check_password(username, password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
