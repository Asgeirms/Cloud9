from django.db import models
from django.contrib.auth.models import AbstractUser
from happenings.models import Event

class User(AbstractUser):
    interests = models.ManyToManyField(Event)
