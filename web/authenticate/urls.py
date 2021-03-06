from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import RegisterCreateView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authenticate/logout.html'), name='logout'),
    path('register/', RegisterCreateView.as_view(), name='register')
]
