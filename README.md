
# Register_Login


https://github.com/user-attachments/assets/363ce4c8-54a0-4375-997d-b21cd7a63503


Este é um projeto Django que implementa um sistema de registro e login de usuários, além de ter validação por email. 

## Funcionalidades

- Registro de novos usuários
- Login de usuários existentes
- Logout de usuários
- Edição de perfil do usuário
- Upload de foto de perfil

## Pré-requisitos

- Python 3.12.3
- Django 5.1.4

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/FelipeAngeli/register_login.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd register_login
   ```

3. Crie um ambiente virtual:

   ```bash
   python3 -m venv venv
   ```

4. Ative o ambiente virtual:

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No Unix ou MacOS:

     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

6. Aplique as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

7. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

8. Acesse o aplicativo no navegador:

   ```
   http://127.0.0.1:8000/
   ```

## Estrutura do Projeto

```plaintext
register_login/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Personalização

- **Templates**: Os templates HTML estão localizados no diretório `accounts/templates/`.
- **Arquivos estáticos**: Os arquivos CSS e JavaScript podem ser adicionados ao diretório `static/`.

## Contato

Para mais informações, visite meu perfil no GitHub: [FelipeAngeli](https://github.com/FelipeAngeli)
