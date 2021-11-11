# blocks the restricted and temporary email logins
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView
from django.forms import ValidationError
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from google.oauth2 import id_token
from google.auth.transport import requests
from .providers import GoogleProviderMod


class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        restricted_list = ['randomemail@gmail.com']
        if email in restricted_list:
            raise ValidationError(
                'You are restricted from registering.'
            )
        return email
    
class GoogleOAuth2AdapterIdToken(GoogleOAuth2Adapter):
    provider_id = GoogleProviderMod.id
    
    def compelte_login(self, request, app, token, *args, **kwargs):
        id_info = id_token.verify_oauth2_token(token.token, request.Request(), app.client_id)    
        
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong user')
        
        extra_data = id_info
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login
    
oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2AdapterIdToken)
oauth2_callback = OAuth2CallbackView.adapter_view(GoogleOAuth2AdapterIdToken)