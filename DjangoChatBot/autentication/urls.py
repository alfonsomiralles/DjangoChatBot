from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='autentication/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    re_path(r'^account_activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_=]+)/$', views.account_activation, name='account_activation'),
    path('request_staff_access/', views.request_staff_access, name='request_staff_access'),
]