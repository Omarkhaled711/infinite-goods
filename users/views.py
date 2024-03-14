from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import url_safe_base64_encode, url_safe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk))
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
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


def activate(request, uidb64, token)
    return HttpResponse()