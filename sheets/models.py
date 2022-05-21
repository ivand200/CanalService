from django.db import models
from django.utils import timezone
from django import forms
from CanalService import settings

# Create your models here.


class Order(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    number = models.IntegerField(null=False, unique=True)
    value = models.FloatField(null=False)
    delivery_time = models.DateField(null=False)
    value_at_rub = models.FloatField(null=False)

    def __str__(self) -> str:
        return self.order


