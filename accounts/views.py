from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from .forms import UserRegisterForm, UserUpdateForm

User = get_user_model()

def handle_form_errors(request, form, error_message="Por favor, corrija os erros abaixo."):
    """
    Adiciona mensagens de erro do formulário.
    """
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f"{field.capitalize()}: {error}")
    messages.error(request, error_message)

def send_verification_email(user_email, user_name):
    """
    Envia um e-mail de verificação após o registro do usuário.
    """
    subject = "Confirmação de Registro"
    message = f"""
    Olá, {user_name}!

    Obrigado por se registrar na nossa aplicação.
    Por favor, clique no link abaixo para confirmar seu e-mail e ativar sua conta:
    
    http://127.0.0.1:8000/activate/{user_email}/
    
    Atenciosamente,
    Equipe Django App
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

def register_view(request):
    form = UserRegisterForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                send_verification_email(user.email, user.first_name)
                messages.success(request, "Registro realizado com sucesso! Verifique seu e-mail para ativar a conta.")
                return redirect("login")  # Redireciona corretamente
            except IntegrityError:
                messages.error(request, "Já existe um usuário com este email.")
        else:
            print("Form errors:", form.errors)  # Log para debug
            handle_form_errors(request, form)
    return render(request, "register.html", {"form": form})

def login_view(request):
    """
    View para login de usuários existentes.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Todos os campos são obrigatórios.")
        else:
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Bem-vindo, {user.first_name}!")
                return redirect(request.GET.get("next", "home"))
            else:
                messages.error(request, "Credenciais inválidas.")

    return render(request, "login.html")

@login_required
def home_view(request):
    """
    View para exibir informações do usuário na página inicial.
    """
    return render(request, "home.html", {"user": request.user})

@login_required
def update_profile_view(request):
    """
    View para atualização do perfil do usuário.
    """
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, f"Perfil de {request.user.first_name} atualizado com sucesso.")
            return redirect("home")
        except IntegrityError:
            messages.error(request, "Erro de integridade ao salvar os dados.")
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
    elif request.method == "POST":
        handle_form_errors(request, form)

    return render(request, "update_profile.html", {"form": form})

def logout_view(request):
    """
    View para logout do usuário.
    """
    logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect("login")

def activate_account(request):
    return HttpResponse("Conta ativada!")