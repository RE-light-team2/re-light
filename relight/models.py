from django.db import models
import datetime

# Create your models here.
class Shop(models.Model):
    """企業側のモデル"""
    name=models.CharField(max_length=256)
    userid=models.CharField(max_length=256)
    password=models.CharField(max_length=256)
    header = models.ImageField(upload_to='images',blank=True, null=True)
    icon = models.ImageField(upload_to='images',blank=True, null=True)

class Customer(models.Model):
    """顧客側のモデル"""
    name=models.CharField(max_length=256)
    userid=models.CharField(max_length=256)
    password=models.CharField(max_length=256)
    header = models.ImageField(upload_to='images',blank=True, null=True)
    icon = models.ImageField(upload_to='images',blank=True, null=True)

class Event(models.Model):
    """開催中のイベントのモデル"""
    title=models.CharField(max_length=256)
    detail=models.TextField(default='')
    created=models.DateTimeField(default=datetime.datetime.now)

