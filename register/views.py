from django.contrib.auth.forms import UserChangeForm
from django.db.models.manager import EmptyManager
from django.http.request import validate_host
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, message
from django.contrib.auth.models import User

from .tokens import account_activation_token


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewUserForm(request.POST or None)
        
        if form.is_valid():
            user = form.save(commit=False)
            # user.email = form.cleaned_data.get('email')
            # # user.is_active()
            user.save()
            
            current_site = get_current_site(request)
            mail_subj = 'Please activate your account'
            
            message = render_to_string(
                'register/activate_mail.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subj, message, to=['to_email']
            )
            email.send()
            return HttpResponse('Please confirm your email address')
        
    else:
        form = NewUserForm()
    
    #         login(request, user)
    #         messages.success(
    #             request, 'Registration Succesful'
    #         )
    #         return redirect('/')
        
    #     else:
    #         messages.error(request, 'Invalid Information, Please try again!')
            
    # form = NewUserForm()
    context = {'register_form': form}
    return render(request, 'register/register.html', context)


def activate(request, uidb64, token, *args, **kwargs):
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        login(request, user)
        messages.success(
            request, 'Email verified, Welcome'
        )
        return redirect('/')
    
    else: 
        messages.error('Sorry, Your Activation has failed!')
        
    context = {'uidb64':uidb64, 'token':token}
    return render(request, 'account/account_activation_email.html', context)
        

def login(request, *args, **kwargs):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST or None)
        
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            login(request, user)
            messages.info(request, f'Welcome {username}')
            return redirect('/')

        else:
            messages.error(request, 'Invalid Username or Password')

    login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'register/login.html', context)


def logout_user(request, *args, **kwargs):
    logout(request)
    messages.info(request, 'Logout Succesful')
    return redirect('/')