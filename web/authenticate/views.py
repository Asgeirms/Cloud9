from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

# Register page for users
def registerView(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Makes user and redirects to login
            return redirect('login')
    else:
        form = UserRegisterForm()
    # Renders a form on the page
    return render(request, 'authenticate/register.html', {'form': form})
