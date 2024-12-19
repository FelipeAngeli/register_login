import pytest
from login_register.models import User
from phonenumber_field.phonenumber import PhoneNumber


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.mark.django_db
def test_create_user(user_data):
    user = User.objects.create_user(**user_data)
    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"]) is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser(user_data):
    superuser = User.objects.create_superuser(**user_data)
    assert superuser.email == user_data["email"]
    assert superuser.check_password(user_data["password"]) is True
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


@pytest.mark.django_db
def test_create_user_without_email(user_data):
    user_data["email"] = None
    with pytest.raises(ValueError, match="O email deve ser definido."):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_str_representation(user_data):
    user = User.objects.create_user(**user_data)
    assert str(user) == user_data["email"]


@pytest.mark.django_db
def test_user_with_optional_fields(user_data):
    user_data.update({
        "phone_number": "+1234567890",
        "gender": "masculino",
    })
    user = User.objects.create_user(**user_data)
    assert user.phone_number == PhoneNumber.from_string("+1234567890")
    assert user.gender == "masculino"


@pytest.mark.django_db
def test_duplicate_email_not_allowed(user_data):
    User.objects.create_user(**user_data)
    with pytest.raises(Exception, match="UNIQUE constraint failed: login_register_user.email"):
        User.objects.create_user(**user_data)


@pytest.mark.django_db
def test_update_user(user_data):
    user = User.objects.create_user(**user_data)
    user.first_name = "Updated"
    user.save()
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.first_name == "Updated"


@pytest.mark.django_db
def test_permissions_and_groups(user_data):
    user = User.objects.create_user(**user_data)
    group = user.groups.create(name="Test Group")
    user.save()
    assert user.groups.filter(name="Test Group").exists()
