# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class URL(models.Model):
    long_url = models.CharField(max_length=100)
    unique_hash = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

@receiver(post_save, sender=URL)
def post_save(sender, instance, created, **kwargs):
    if created:
        instance.unique_hash = '{0:08d}'.format(instance.pk)
        instance.save()
