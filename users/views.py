from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import RegisterForm
from material.models import StudentHonor

User = get_user_model()

def _ensure_honor(user):
    if not user.is_authenticated:
        return None
    obj, _ = StudentHonor.objects.get_or_create(user=user)
    return obj

@login_required
def profile_view(request):
    honor = _ensure_honor(request.user)
    return render(request, 'users/profile.html', {'honor': honor})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('users:activate', kwargs={'uidb64': uidb64, 'token': token})
            )

            message = render_to_string('users/verify_now.html', {
                'user': user,
                'activation_link': activation_link,
            })
            mail_subject = 'Activate your account'
            email = EmailMessage(mail_subject, message, to=[form.cleaned_data['email']])
            email.content_subtype = "html"
            email.send()

            messages.success(request, "Verification email sent. Check your inbox.")
            return render(request, 'users/verify_sent.html')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0] if settings.AUTHENTICATION_BACKENDS else None)
        _ensure_honor(user)
        messages.success(request, "Your account has been activated.")
        return render(request, 'users/verified.html')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return render(request, 'users/verify_failed.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Please verify your email before logging in.")
            else:
                login(request, user)
                return redirect('material:home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('material:home')
