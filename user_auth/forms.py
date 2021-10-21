from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


date = datetime.date.today()
year = date.strftime('%Y')
int_year = int(year) + 1    # converting to int and the +1 will match the current year.

YEARS = [x for x in range(1910, int_year)]

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Optional')
    last_name = forms.CharField(max_length=50,required=False, help_text='Optional')
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address')
    birthday = forms.DateField(
        label='What is your birth date?',
        initial='2000-01-01',
        widget=forms.SelectDateWidget(years=YEARS)
        )
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'password2',
        )
        
        