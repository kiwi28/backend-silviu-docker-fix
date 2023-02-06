# models.py
from django.db import models
from accounts.models import CustomUser


class Categories(models.Model):
    name = models.CharField(max_length=60)
    user = models.ForeignKey(CustomUser, default=None, blank=True, null=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name
