from django.shortcuts import render
from .forms import RegisterForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, user_name=user_name, password=password)
            user.phone_number = phone_number
            user.save()
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def login(request):
    return render(request, 'login.html')

def logout(request):
    return
