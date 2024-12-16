from django.db import models
from django_summernote.fields import SummernoteTextField


class Subscriber(models.Model):
    """
    Stores a single subscriber
    """
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    """
    Stores a single newsletter instance
    related to :model:`newsletter.Subscriber`
    """
    subject = models.CharField(max_length=255)
    content = SummernoteTextField()
    recipients = models.ManyToManyField(Subscriber)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
