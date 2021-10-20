from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from mysite.views import create_blog, blog_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('blog/', create_blog),
    path('blog/<int:pk>/', blog_view),
    
    path('logout', include('allauth.urls')),
    
    path('admin/', admin.site.urls),
]
