from django.core.mail import send_mail
from django.conf import settings

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