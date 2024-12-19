import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "first_name": "Test",
        "password": "password123",
        "confirm_password": "password123",
        "phone_number": "+12125552368",
    }

@pytest.fixture
def existing_user(db):
    return User.objects.create_user(
        email="existinguser@example.com",
        password="password123",
        first_name="Existing",
        phone_number="+1234567890",
    )

@pytest.fixture
def client():
    from django.test import Client
    return Client()

# Testes de RegisterView
@pytest.mark.django_db
class TestRegisterView:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.register_url = reverse("register")

    def test_register_successful(self, user_data):
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == 302
        assert response.url == reverse("login")

    def test_register_empty_email(self, user_data):
        user_data["email"] = ""
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == 200
        assert "Por favor, corrija os erros abaixo." in response.content.decode()
        assert "Email:" in response.content.decode()

    def test_register_password_mismatch(self, user_data):
        user_data["confirm_password"] = "wrongpassword"
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == 200
        assert "Por favor, corrija os erros abaixo." in response.content.decode()
        assert "As senhas não coincidem." in response.content.decode()

    def test_register_existing_user(self, existing_user, user_data):
        user_data["email"] = existing_user.email
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == 200
        assert "Este email já está registrado." in response.content.decode()
