from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
import datetime
from django.core.mail import send_mail, EmailMessage

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

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Shop_Profile(models.Model):
    """企業のモデル"""
    shop = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, unique=True)
    self_introduction = models.CharField(blank=True, max_length=500)
    icons = models.ImageField(upload_to="icons/")
    headers = models.ImageField(upload_to="headers/")
    online_address = models.URLField(max_length=255)
    plan = models.CharField(max_length=10)


class Cus_Profile(models.Model):
    """顧客のモデル"""
    cus = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, unique=True)
    self_introduction = models.CharField(blank=True, max_length=500)
    icons = models.ImageField(upload_to="icons/")
    headers = models.ImageField(upload_to="headers/")
    gender = models.CharField(max_length=10)


class Event(models.Model):
    """開催中のイベントのモデル"""
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="event/", unique=True)
    title = models.CharField(max_length=256, unique=True)
    detail = models.CharField(max_length=1000)
    questionnaire_url = models.CharField(blank=True, max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    active = models.BooleanField(default=False)
