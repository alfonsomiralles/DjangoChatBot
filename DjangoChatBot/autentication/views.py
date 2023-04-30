from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import base64
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactiva el usuario hasta que hagan clic en el enlace de confirmación
            if 'is_staff_request' in request.POST and request.POST['is_staff_request'] == 'on':
                user.is_staff = False
                user.save()
                send_staff_request_email(request, user)
            else:
                user.save()
            send_confirmation_email(request, user)
            messages.success(request, 'Te has registrado con éxito. Por favor, revisa tu email para confirmar su cuenta')
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return redirect('register')
    else:
        form = CustomUserCreationForm
    context = {
        'form': form
    }
    return render(request, 'autentication/register.html', context)

def send_staff_request_email(request, user):
    subject = 'Solicitud de acceso al staff'
    message = 'El usuario {username} ha solicitado acceso al staff. Revisa las solicitudes pendientes en el panel de administración para aprobar o rechazar esta solicitud.'.format(username=user.username)
    send_mail(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['pmsdjango@gmail.com'], fail_silently=False)

@login_required
def request_staff_access(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_staff_request:
            user.is_staff_request = True
            user.save()
            send_staff_request_email(request, user)
            messages.success(request, 'Solicitud de acceso al staff enviada con éxito.')
        else:
            messages.info(request, 'Ya has enviado una solicitud de acceso al staff. Por favor, espera a que sea revisada.')
        return redirect('profile')
    else:
        return render(request, 'autentication/index.html')

def send_confirmation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = force_str(base64.urlsafe_b64encode(force_bytes(user.pk)))
    link = request.build_absolute_uri(reverse('account_activation', kwargs={'uidb64': uid, 'token': token}))

    subject = 'Activa tu cuenta y para utilizar ChatBot'
    message = render_to_string('autentication/account_activation_email.html', {'link': link, 'username': user.username})
    send_mail(subject, '', from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email], html_message=message)


def account_activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_decoded = force_str(base64.urlsafe_b64decode(token.encode()))

    if user is not None and token_decoded == force_str(user.pk):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada con éxito. Ahora puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación no es válido o ha expirado.')
        return redirect('register')
    

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.is_staff_request = True
        user.save()
        send_staff_request_email(request, user)
        messages.success(request, 'Solicitud de acceso al staff enviada con éxito.')
        return redirect('profile')

    return render(request, 'autentication/profile.html')
