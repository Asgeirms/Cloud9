from django.db import models
from django.contrib.auth.models import AbstractUser

from happenings.models import Schedule


class User(AbstractUser):
    swiped_events = models.ManyToManyField(Schedule)
