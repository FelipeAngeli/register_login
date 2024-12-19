from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyCustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name=None, phone_number=None, gender=None, password=None):
        if not email:
            raise ValueError('O email deve ser definido.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name=None, phone_number=None, gender=None):
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
    GENDER_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('outro', 'Outro'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = None
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
        return self.email