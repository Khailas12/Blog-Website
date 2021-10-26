from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = NewUserForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            # user.email = form.cleaned_data.get('email')
            # # user.is_active()
            # user.save()
            
            login(request, user)
            messages.success(
                request, 'Registration Succesful'
            )
            return redirect('/')


        messages.error(request, 'Invalid Information, Please try again!')
    form = NewUserForm()

    context = {'register_form': form}
    return render(request, 'register/register.html', context)


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
