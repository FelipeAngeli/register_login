from django import forms
from .models import User 

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"}),
        label="Senha",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirme sua senha"}),
        label="Confirme a senha",
    )

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Digite seu nome"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Digite seu email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem.")

        return cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_picture', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu nome',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Digite seu sobrenome',
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
            raise forms.ValidationError("Este email já está registrado.")
        return email

    def clean(self):
        """
        Valida a confirmação de senha.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'profile_picture']
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
