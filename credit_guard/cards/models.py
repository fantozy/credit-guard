from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    censored_number = models.CharField(max_length=16)
    is_valid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.censored_number
