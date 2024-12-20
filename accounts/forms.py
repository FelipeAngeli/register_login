from django import forms
from .models import User
from phonenumbers import parse, NumberParseException, PhoneNumberFormat, format_number, is_valid_number


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

    def clean_email(self):
        """
        Valida se o email já está registrado.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está registrado.")
        return email


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

def clean_phone_number(self):
    """
    Valida e ajusta o número de telefone para o formato internacional.
    """
    phone_number = self.cleaned_data.get('phone_number')
    print(f"Phone number recebido: {phone_number}")

    if not phone_number:
        raise forms.ValidationError("Por favor, insira um número de telefone.")

    try:
        # Converte o número de telefone para string, se necessário
        phone_number_str = str(phone_number)
        
        # Adiciona o código do país "BR" se necessário
        parsed_number = parse(phone_number_str, "BR")
        
        if not is_valid_number(parsed_number):
            raise forms.ValidationError("Por favor, insira um número de telefone válido.")

        # Retorna o número formatado no padrão internacional
        formatted_number = format_number(parsed_number, PhoneNumberFormat.E164)
        print(f"Phone number processado: {formatted_number}")
        return formatted_number
    except NumberParseException as e:
        print(f"Erro ao processar número: {e}")
        raise forms.ValidationError("Por favor, insira um número de telefone válido.")
    