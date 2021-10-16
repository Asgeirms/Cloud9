from django.db import models
from django.contrib.auth.models import AbstractUser

from happenings.models import Schedule

class User(AbstractUser):
    # Adding interest interaction to a schedule
    interested_events = models.ManyToManyField(Schedule, related_name="users")
    