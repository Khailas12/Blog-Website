from django.shortcuts import render
from django.conf import settings
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib import xsrfutil
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from googleapiclient.discovery import build
from .models import CredentialsModel
import httplib2
from dotenv import load_dotenv
import os


CLIENT_SECRETS = settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON

load_dotenv()
GOOGLE_CONSOLE_KEY = os.getenv('MY_GOOGLE_CONSOLE_KEY')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent'
    )


def gmail_authenticate(request, *args, **kwrgs):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    
    if credential is None or credential.invalid is True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        
        authorize_url = FLOW.step1_get_authorize_url()
        # f = FLOW(id=request.user, flow=FLOW)
        # f.save()
        return HttpResponseRedirect(authorize_url)
    
    else:
        http = httplib2.Http()  # handles caching, keep alive, compression, redirects etc.
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http, developerKey=GOOGLE_CONSOLE_KEY)
        print('access_token = ', credential.access_token)
        status = True
        
        context = {'status': status}
        return render(request, 'index.html', context)
    
    
    
# callback url
def auth_return(request, *args, **kwargs):
    str_state = request.GET.get('state')
    get_state = bytes(str_state, encoding='utf-8')
    # is_private = str(request.GET.get['state'])
    
    if not xsrfutil.validate_token(
        settings.SECRET_KEY, get_state, request.user
        ):  # validates token with secret key
        return HttpResponseBadRequest()           # 400 status code. request could not be understood by server cz of malformed syntax
    
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    
    print('access_token: % s' % credential.access_token)
    return HttpResponseRedirect('/')
    
    
# checks whether the user is logged in or not
def user_check(request, *args, **kwargs):
    status = True   # if user has already logged in frm ggl
    
    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin')
    
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    
    try:
        access_token = credential.access_token
        resp, cont = httplib2.Http().request(
            'https://www.googleapis.com/auth/gmail.readonly',
            headers={
                'Host': 'www.googleapis.com',
                'Authorization': access_token
            }
        )
    
    except:
        status = False
        print('Not found')
    
    context = {'status': status}
    return render(request, 'google_auth/main_auth.html', context)