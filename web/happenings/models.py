from django.db import models
from django.conf import settings


class GeneratedShortDescriptions(models.Model):
    """Model for generated short descriptions.
        Generated short descriptions are clickbait like taglines that admins can create
        and event hosts can choose from to add to their event"""
    description = models.TextField(max_length=250)

    def __str__(self):
        return str(self.description)


class InterestCategory(models.Model):
    """Model for Interest categories.
        Interest categories are categories that describe the event's content (like "music" or "outdoor"), and are used
        to influence the suggestions made by the 'AI'"""
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return str(self.name)


class RequirementCategory(models.Model):
    """Model for Requirement categories.
        Requirement categories are categories that describe the avalibility for the event (like 'Vegan',
         'English friendly' or 'Wheelchair friendly'). Requirement categories can be used
         by users to filter by"""
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500)

    def __str__(self):
        return str(self.name)


class CategoryWeightsUser(models.Model):
    """Model for CategoryWeightsUser.
        CategoryWeightsUser are used by the AI to influence the events that are shown"""
    category = models.ForeignKey(
        InterestCategory,
        on_delete=models.CASCADE)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    weight = models.FloatField(default=1)


class Event(models.Model):
    """Model for Events"""

    class Status(models.TextChoices):
        PENDING = 'P', "Pending"
        APPROVED = 'A', "Approved"
        DISAPPROVED = 'N', "Disapproved"
        DELETED = 'D', "Deleted"

    STATUS_CHOICES_DICT = dict(Status.choices)

    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)
    short_description = models.TextField(blank=True, max_length=250)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='events')
    admin_approved = models.CharField(choices=Status.choices, max_length=2, default=Status.PENDING)
    interest_categories = models.ManyToManyField(InterestCategory, blank=True)
    requirement_categories = models.ManyToManyField(RequirementCategory, blank=True)

    generated_short_description = models.ForeignKey(
        GeneratedShortDescriptions,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)

    def get_pricerange(self):
        if self.max_price > 0:
            return str(self.min_price) + "kr - " + str(self.max_price) + "kr"
        return "FREE"

    def get_status(self):
        if self.admin_approved == Event.Status.DELETED:
            return "Deleted by admin"
        return self.STATUS_CHOICES_DICT[self.admin_approved]


class Schedule(models.Model):
    """Model for schedule"""
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
