from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import get_default_password_validators

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,label=_('Correo electrónico'))
    username = forms.CharField(label=_('Nombre de usuario'))
    password1 = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmar contraseña'), widget=forms.PasswordInput)
    is_staff_request = forms.BooleanField(
        required=False,
        initial=False,
        label=_('¿Solicitar acceso al staff?')
    )
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email
    
    def get_password_help_texts():
        help_texts = []
        for validator in get_default_password_validators():
            help_texts.append(validator.get_help_text())
        return help_texts
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')   
         
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']    

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Contraseña actual"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )        