from django.shortcuts import render
from django.conf import settings
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib import xsrfutil
from django.http import HttpResponseRedirect
from googleapiclient.discovery import build
from .models import CredentialsModel
import httplib2


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent'
    )


def gmail_authenticate(request, *args, **kwrgs):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    
    else:
        http = httplib2.Http()  # handles caching, keep alive, compression, redirects etc.
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http)
        print('access_token = ', credential.access_token)
        status = True
        
        context = {'status': status}
        return render(request, 'index.html', context)