from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from mysite.views import create_blog, blog_view, home_view
from django.contrib.auth.views import LogoutView
from user_auth import views as auth_view
from django.conf.urls import url
from google_auth import views as g_view
from register.views import register, login, logout_user, activate


urlpatterns = [
    path('', home_view),
    path('blog/', create_blog, name='blog'),
    path('blog/<int:pk>/', blog_view, name='blog_vie'),

    url(r'^register/$', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),

    path('accounts/', include('allauth.urls')),

    path('activate/<uidb64>/<token>/', activate, name='activate'),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,name='activate'),

    url(r'^gmailAuthenticate/', g_view.gmail_authenticate, name='gmailauth'),
    url(r'^oauth2callback/', g_view.auth_return),
    url(r'^$ghome/', g_view.user_check),

    url(r'^signup/$', auth_view.signup, name='signup'),
    # path('signup/', auth_view.signup, name='signup'),
    path('sent/', auth_view.activation_sent_view, name='activation_sent'),
    # path('activate/<slug:uidb64>/<slug:token>', auth_view.activate, name='activate'),

    path('admin/', admin.site.urls),
]

#  path() always matches the complete path, so path('account/login/') is equivalent to url('^account/login/$').