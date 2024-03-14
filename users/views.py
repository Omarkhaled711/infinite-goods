from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


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
            messages.success(request, 'Registration successful.')
            return redirect('register')
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login cerdentials')
            return redirect('login')
    return render(request, 'login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')
