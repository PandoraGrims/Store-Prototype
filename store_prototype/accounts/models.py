from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

from django.contrib.auth import get_user_model


class MyUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'my_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
