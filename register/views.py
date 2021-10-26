from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST or None)
        
        if form.is_valid(commit=False):
            user = form.save()
            
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            
            login(request, user)
            messages.success(
                request, 'Registration Succesful'
            )
            return redirect('/')
        
        else:
            messages.error(request, 'Invalid Information, Please try again!')
        
    form = NewUserForm()
    context = {'register_form': form}
    return render(request, 'register.html', context)