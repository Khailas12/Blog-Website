from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from mysite.views import create_blog



urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('blog/', create_blog),
    path('admin/', admin.site.urls),
]
