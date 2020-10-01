from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Customer_SignUpForm(UserCreationForm):
    user_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='名前'
    )
    user_id = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='利用者ID'
    )
    self_introduction = forms.CharField(
        max_length=500,
        required=False,
        help_text='オプション',
        label='自己紹介文'
    )
    gender = forms.CharField(
        max_length=2,
        required=False,
        help_text='オプション',
        label='性別'
    )
    email = forms.EmailField(
        max_length=254,
        help_text='必須 有効なメールアドレスを入力してください。',
        label='Eメールアドレス'
    )
    icon = forms.ImageField(
        label = "アイコン"
    )
    header = forms.ImageField(
        label = "ヘッダー"
    )

    class Meta:
        model = User
        fields = ('username', 'user_id',  'email', 'gender','self_introduction', 'icon', 'header', 'password1', 'password2', )

class Shop_SignUpForm(UserCreationForm):
    user_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='名前'
    )
    user_id = forms.CharField(
        max_length=30,
        required=False,
        help_text='オプション',
        label='利用者ID'
    )
    self_introduction = forms.CharField(
        max_length=500,
        required=False,
        help_text='オプション',
        label='自己紹介文'
    )
    icon = forms.ImageField(
        label = "アイコン"
    )
    header = forms.ImageField(
        label = "ヘッダー"
    )

    class Meta:
        model = User
        fields = ('username', 'user_id', 'self_introduction', 'icon', 'header', 'password1', 'password2', )