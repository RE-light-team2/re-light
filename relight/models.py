from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
import datetime

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, password, userid):

        user = self.model(
            userid=userid,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, userid):
        user = self.create_user(
            userid=userid,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser, PermissionsMixin):
    """ユーザーのモデル"""
    email = models.EmailField(max_length=255, unique=True)
    s_or_c = models.CharField(max_length=10)
    userid = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'userid'
    EMAIL_FIELD = 'email'


class Shop_Profile(models.Model):
    """企業のモデル"""
    shop = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, unique=True)
    self_introduction = models.CharField(max_length=500)
    icons = models.ImageField(upload_to="icons/", unique=True)
    headers = models.ImageField(upload_to="headers/", unique=True)
    online_address = models.URLField(max_length=255)
    plan = models.CharField(max_length=10)


class Cus_Profile(models.Model):
    """顧客のモデル"""
    cus = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, unique=True)
    self_introduction = models.CharField(max_length=500)
    icons = models.ImageField(upload_to="icons/", unique=True)
    headers = models.ImageField(upload_to="headers/", unique=True)
    gender = models.CharField(max_length=10)


class Event(models.Model):
    """開催中のイベントのモデル"""
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="event/", unique=True)
    title = models.CharField(max_length=256)
    detail = models.CharField(max_length=500)
    questionnaire_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now)
