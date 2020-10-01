from django.db import models
import datetime

# Create your models here.

class Image(models.Model):
   id = models.IntegerField(primary_key=True)
   objects = models.Manager
   origin = models.ImageField(upload_to="photos/%y/%m/%d/")

class Shop(models.Model):
    """企業側のモデル"""
    name=models.CharField(max_length=256)
    userid=models.CharField(max_length=256)
    password=models.CharField(max_length=256)
    self_introduction = models.CharField(max_length=500)
    header = models.ImageField(upload_to='imgs/')
    icon = models.ImageField(upload_to='imgs/')

class Customer(models.Model):
    """顧客側のモデル"""
    name=models.CharField(max_length=256)
    userid=models.CharField(max_length=256)
    password=models.CharField(max_length=256)
    gender = models.CharField(max_length=2)
    email = models.EmailField(max_length=75)
    self_introduction = models.CharField(max_length=500)
    header = models.ImageField(upload_to='imgs/')
    icon = models.ImageField(upload_to='imgs/')

class Event(models.Model):
    """開催中のイベントのモデル"""
    title = models.CharField(max_length=256)
    detail = models.CharField(max_length=500)
    created = models.DateTimeField(default=datetime.datetime.now)



