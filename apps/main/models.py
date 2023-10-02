"""CUSTOM LIBS"""
import datetime

"""MODELS AUTHS"""
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        if not email:
            raise ValidationError('Email required')

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return


class MyUser(AbstractBaseUser, PermissionsMixin):
    class UserStatus(models.TextChoices):
        TEACHER = 'Учитель'
        STUDENT = 'Студент'
    name = models.CharField(
        verbose_name='Имя',
        max_length=25
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=25
    )
    father_name = models.CharField(
        verbose_name='Отчество',
        max_length=25
    )
    email = models.EmailField(
        widget=forms.EmailInput({'placeholder': 'test@example.com'})
    )
    status = models.Choices(
        choices=UserStatus.choices,
        default=UserStatus.STUDENT
    )
    date_of_birth = models.DateField(
        default=datetime.datetime.now()
    )
    avatar = models.ImageField(
        default='images/default.jpg'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

