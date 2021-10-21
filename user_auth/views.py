from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm



def signup(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            the_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, passsword=the_password)
            
            login(request, user)
            return redirect('/')
            
    else:
        form = SignUpForm()
    
        context = {'form': form}
        return render(request, 'user_auth/signup.html', context)