from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager,AbstractBaseUser
import datetime

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, s_or_c,name,gender,self_introduction,icons,headers,password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            gender = gender,
            name = name,
            s_or_c = s_or_c,
            icons = icons,
            headers = headers,
            self_introduction = self_introduction,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

def create_superuser(self, email,s_or_c,name,gender,self_introduction,icons,headers,password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            gender = gender,
            name = name,
            s_or_c = s_or_c,
            icons = icons,
            headers = headers,
            self_introduction = self_introduction,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserInfo(AbstractBaseUser, PermissionsMixin):
    """ユーザーのモデル"""  
    s_or_c = models.CharField(max_length=10)
    email = models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=30,unique=True) 
    gender = models.CharField(max_length=10)
    self_introduction = models.CharField(max_length=500)
    icons = models.ImageField(upload_to="icons/",unique=True)
    headers = models.ImageField(upload_to="headers/",unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)   
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    

class Event(models.Model):
    """開催中のイベントのモデル"""
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="event/",unique=True)
    title = models.CharField(max_length=256)
    detail = models.CharField(max_length=500)
    questionnaire_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now)



