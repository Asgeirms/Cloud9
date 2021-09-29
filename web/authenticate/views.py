from .forms import UserRegisterForm
from django.views.generic.edit import CreateView
from .models import User
from django.urls import reverse_lazy

# Register page for users
class RegisterCreateView(CreateView):
    template_name = "authenticate/register.html"
    models = User
    form_class = UserRegisterForm
    context_object_name = "user"
    success_url = reverse_lazy('login')
