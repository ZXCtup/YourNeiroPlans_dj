from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.TextField(verbose_name='Телефон', null=True, blank=True)
    bio = models.TextField(verbose_name='О себе', null=True, blank=True)
