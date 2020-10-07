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
            email,
            password=password,
            gender = gender,
            name = name,
            s_or_c = s_or_c,
            icons = icons,
            headers = headers,
            self_introduction = self_introduction,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserInfo(AbstractBaseUser, PermissionsMixin):
    """ユーザーのモデル"""  
    s_or_c = models.CharField(max_length=2,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=30,unique=True) 
    gender = models.CharField(max_length=2,unique=True)
    self_introduction = models.CharField(max_length=500,unique=True)
    icons = models.ImageField(upload_to="icons/",verbose_name='アイコン',unique=True)
    headers = models.ImageField(upload_to="headers/",verbose_name='アイコン',unique=True)
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Event(models.Model):
    """開催中のイベントのモデル"""
    title = models.CharField(max_length=256)
    detail = models.CharField(max_length=500)
    created = models.DateTimeField(default=datetime.datetime.now)



