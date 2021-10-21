from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm



def signup(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        
        if form.is_valid():
            user = form.save()
            
            user.refresh_form_db()  # loads the profile instance created by signal
            user.profile.birthday = form.cleaned_data.get('birthday')

            username = form.cleaned_data.get('username')
            the_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, passsword=the_password)
            
            login(request, user)
            return redirect('/')
            
    else:
        form = SignUpForm()
    
        context = {'form': form}
        return render(request, 'user_auth/signup.html', context)