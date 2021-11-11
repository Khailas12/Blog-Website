# blocks the restricted and temporary email logins
from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError


class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        restricted_list = ['randomemail@gmail.com']
        if email in restricted_list:
            raise ValidationError(
                'You are restricted from registering.'
            )
        return email