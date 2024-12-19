from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyCustomUserManager(BaseUserManager):
    """
    Custom Manager para o modelo User sem o campo de username.
    """

    def create_user(self, email, first_name, last_name=None, phone_number=None, gender=None, password=None):
        """
        Cria um usuário padrão com os campos fornecidos.
        """
        if not email:
            raise ValueError("O email deve ser definido.")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
        )
        if password:
            user.set_password(password)
        else:
            raise ValueError("A senha deve ser definida.")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password, last_name=None, phone_number=None, gender=None):
        """
        Criação de superusuário com privilégios administrativos.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """
    Modelo customizado de usuário que substitui o username pelo email como identificador único.
    """
    GENDER_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('outro', 'Outro'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = None  # Remove o campo username do modelo padrão
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        default=None
    )
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    objects = MyCustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        """
        Retorna a representação do objeto com o email do usuário.
        """
        return self.email
