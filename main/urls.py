from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from mysite.views import create_blog, blog_view
from django.contrib.auth.views import LogoutView
from user_auth import views as core_views


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('blog/', create_blog),
    path('blog/<int:pk>/', blog_view),
    
    path(r'^signup/$', core_views.signup),
    path('admin/', admin.site.urls),
]
