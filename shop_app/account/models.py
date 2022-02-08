import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None):
        if not email:
            raise ValueError('User must have a valid email.')

        user = self.model(email=self.normalize_email(email), # normalize_email forces all characters to be lowercase.
                          name=name,
                          surname=surname)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, surname, password):
        user = self.create_user(
            email=email,
            name=name,
            surname=surname,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self.db)
        return user

class Account(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(verbose_name='e-mail', max_length=60, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def __str__(self):
        return f'{self.surname},{self.name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
