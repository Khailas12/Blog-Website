from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


date = datetime.date.today()
year = date.strftime('%Y')
int_year = int(year) + 1

YEARS = [x for x in range(1910, int_year)]


class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    birthday = forms.DateField(
        label='Birthday',
        initial='2000-01-01',
        widget=forms.SelectDateWidget(years=YEARS)
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'birthday',
        ]
        
    def save(self, commit, *args, **kwargs):
        user = super(NewUserForm, self).save(commit=False, *args, **kwargs)
        user.email = self.cleaned_data['email']

        return user