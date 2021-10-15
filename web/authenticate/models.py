from django.db import models
from django.contrib.auth.models import AbstractUser

from happenings.models import Schedule

class User(AbstractUser):
    # Adding interest interaction to a schedule
    interests = models.ManyToManyField(Schedule)
    pass
