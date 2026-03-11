from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

def avatar_upload_to(instance, filename):
    return f"avatars/{instance.email}/{filename}"

class PerfilManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Perfil(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        default= "default/default.png",
        blank=True,
        null = True,
        verbose_name="Avatar"
    )
    direccion = models.CharField(max_length=100, null=True, blank=True)
    celular = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'  # El email ahora es el login
    REQUIRED_FIELDS = ['first_name','last_name']      # Por defecto pide 'email' y 'password', quita 'username' de aquí

    objects = PerfilManager()

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"