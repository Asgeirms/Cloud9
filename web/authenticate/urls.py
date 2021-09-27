from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import registerView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', registerView, name='register')
]
