from django.db import models
from django.conf import settings

class InterestCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    def __str__(self):
        return str(self.name)

class RequirementCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    def __str__(self):
        return str(self.name)

class CategoryWeightsUser(models.Model):
    category = models.ForeignKey(
        InterestCategory,
        on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    weight = models.FloatField(default=1)

class Event(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)
    short_description = models.TextField(blank=True, max_length=250)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='events')
    admin_approved = models.BooleanField(default=False)
    interest_categories = models.ManyToManyField(InterestCategory, blank=True)
    requirement_categories = models.ManyToManyField(RequirementCategory, blank=True)

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True # Making it optinal
    )

    def __str__(self):
        return str(self.name)

    def get_pricerange(self):
        if self.max_price > 0:
            return str(self.min_price) + "kr - " + str(self.max_price) + "kr"
        return "FREE"

class Schedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.event.name + "-" + self.start_time.strftime('%Y-%m-%d %H:%M'))

    def get_times(self):
        if self.start_time.strftime('%d-%m-%Y') != self.end_time.strftime('%d-%m-%Y'):
            return str(self.start_time.strftime('%d-%m-%Y - %H:%M') + " to " +
                       self.end_time.strftime('%d-%m-%Y - %H:%M'))
        return str(self.start_time.strftime('%d-%m-%Y %H:%M') + " to " + self.end_time.strftime('%H:%M'))
