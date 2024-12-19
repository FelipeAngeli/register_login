from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()


class BasePhoneValidationMixin:
    """
    Mixin para validação de número de telefone.
    """
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve estar no formato '+999999999'. Até 15 dígitos permitidos."
    )

    def clean_phone_number(self):
        """
        Limpa e valida o campo de número de telefone.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            self.phone_validator(phone_number)
        return phone_number

class UserRegisterForm(forms.ModelForm, BasePhoneValidationMixin):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha',
            'class': 'form-control'
        }),
        label="Confirme sua senha"
    )

    class Meta:
        model = User
        fields = ['first_name', 
                  'email', 
                  'phone_number', 
                  'gender', 
                  'profile_picture', 
                  'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Digite seu email',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Digite seu telefone',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Digite sua senha',
                'class': 'form-control'
            }),
        }

    def clean_email(self):
        """
        Valida se o email já está registrado.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está registrado.")
        return email

    def clean(self):
        """
        Valida a confirmação de senha e outros campos.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")

        return cleaned_data

class UserUpdateForm(forms.ModelForm, BasePhoneValidationMixin):
    class Meta:
        model = User
        fields = ['first_name', 
                  'last_name', 
                  'phone_number', 
                  'gender', 
                  'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu sobrenome',
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Digite seu telefone',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
