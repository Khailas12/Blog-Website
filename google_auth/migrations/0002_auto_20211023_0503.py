# Generated by Django 3.2.7 on 2021-10-22 23:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2client.contrib.django_util.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('google_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentialsmodel',
            name='credential',
            field=oauth2client.contrib.django_util.models.CredentialsField(null=True),
        ),
        migrations.AlterField(
            model_name='credentialsmodel',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
