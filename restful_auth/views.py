from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.views.decorators.csrf import csrf_exempt
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView

from .adapter import GoogleOAuth2AdapterIdToken


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2AdapterIdToken
    callback_url = 'http://localhost:8000/api/v1/users/login/google/callbak'
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
    
    def get_serializer(self, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(**kwargs)
    
google_login = GoogleLoginView.as_view()