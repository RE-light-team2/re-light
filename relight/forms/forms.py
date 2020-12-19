from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from relight.models import UserInfo, Shop_Profile, Cus_Profile, Event
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


class Create_UserInfo_Form(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['userid', 'password1', 'password2', 'email']

    password1 = forms.CharField(label='PASSWORD', max_length=128, widget=forms.PasswordInput(
        attrs={'placeholder': 'パスワードを入力してください', 'class': 'form-control', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='PASSWORDCONFIRM', max_length=128, widget=forms.PasswordInput(
        attrs={'placeholder': 'パスワードを再度入力してください', 'class': 'form-control', 'autocomplete': 'off'}))
    error_message = 'error'
    userid = forms.CharField(required=True, label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '利用者IDを入力してください', 'class': 'form-control'}))
    email = forms.EmailField(max_length=255, label='EMAIL', required=True)

    def clean_userid(self):
        userid = self.cleaned_data['userid']
        if ' ' in userid:
            raise forms.ValidationError('Userid should not contain any space')
        if '　' in userid:
            raise forms.ValidationError('Userid should not contain any space')
        return userid

    def clean_email(self):
        email = self.cleaned_data['email']
        if ' ' in email:
            raise forms.ValidationError('Email should not contain any space')
        if '　' in email:
            raise forms.ValidationError('Email should not contain any space')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if ' ' in password1:
            raise forms.ValidationError(
                'Password should not contain any space')
        return password1

    def save(self, post, s_c, commit=True):
        user = super(Create_UserInfo_Form, self).save(commit=False)
        user.userid = post["userid"]
        user.email = post["email"]
        if s_c == "shop":
            user.s_or_c = "shop"
        else:
            user.s_or_c = "cus"
        if commit:
            user.save()
        return user


class Create_Shop_Form(forms.ModelForm):
    class Meta:
        model = Shop_Profile
        fields = ['name', 'icons', 'headers',
                  'online_address', 'self_introduction']
    name = forms.CharField(label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '名前を入力してください', 'class': 'form-control'}))
    icons = forms.ImageField()
    headers = forms.ImageField()
    error_message = 'error'
    online_address = forms.URLField()
    PLAN = [('Light Plan', 'ライトプラン'), ('Basic Plan',
                                       'ベーシックプラン'), ('Premium Plan', 'プレミアムプラン')]
    plan = forms.ChoiceField(choices=PLAN, widget=forms.RadioSelect())
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION',
                                        max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    is_save = False

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise forms.ValidationError('Name should not contain any space')
        if '　' in name:
            raise forms.ValidationError('Name should not contain any space')
        return name

    def clean_online_address(self):
        address = self.cleaned_data['online_address']
        if ' ' in address:
            raise forms.ValidationError(
                'OnlineAddress should not contain any space')
        if '　' in address:
            raise forms.ValidationError(
                'OnlineAddress should not contain any space')
        return address

    def save(self, post, file, user, commit=True):
        profile = super(Create_Shop_Form, self).save(commit=False)
        profile.name = post["name"]
        profile.icons = file["icons"]
        profile.headers = file["headers"]
        profile.self_introduction = post["self_introduction"]
        profile.online_address = post["online_address"]
        profile.plan = post["plan"]
        profile.shop = user
        if commit:
            profile.save()
        return profile


class Create_Cus_Form(forms.ModelForm):
    class Meta:
        model = Cus_Profile
        fields = ['name', 'icons', 'headers', 'gender', 'self_introduction']

    name = forms.CharField(label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '名前を入力してください', 'class': 'form-control'}))
    icons = forms.ImageField()
    headers = forms.ImageField()
    error_message = 'error'
    GENDER = [('man', '男性'), ('woman', '女性'), ('No', '未回答')]
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION',
                                        max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    is_save = False

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise forms.ValidationError('Name should not contain any space')
        if '　' in name:
            raise forms.ValidationError('Name should not contain any space')
        return name

    def save(self, post, file, user, commit=True):
        profile = super(Create_Cus_Form, self).save(commit=False)
        profile.name = post["name"]
        profile.icons = file["icons"]
        profile.headers = file["headers"]
        profile.self_introduction = post["self_introduction"]
        profile.gender = post["gender"]
        profile.cus = user
        if commit:
            profile.save()
        return profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['userid', 'password']

    userid = forms.CharField(max_length=30, label='USER_ID', required=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        for field in self.fields.values():
            print(field.widget)
            field.widget.attrs['placeholder'] = field.label


class Create_Event_Form(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "detail", "questionnaire_url", "image")

    image = forms.ImageField()
    title = forms.CharField(label='TITLE', max_length=256, widget=forms.TextInput(
        attrs={'placeholder': 'タイトルを入力してください', 'class': 'form-control'}))
    detail = forms.CharField(label='DETAIL',  max_length=1000, widget=forms.Textarea(
        attrs={'rows': 5, 'class': 'form-control'}))
    questionnaire_url = forms.CharField(label='URL', max_length=500, widget=forms.TextInput(
        attrs={'placeholder': 'アンケート用のURLを入力してください', 'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if ' ' in title:
            raise forms.ValidationError('Name should not contain any space')
        if '　' in title:
            raise forms.ValidationError('Name should not contain any space')
        return title

    def clean_online_address(self):
        questionnaire_url = self.cleaned_data['questionnaire_url']
        if ' ' in questionnaire_url:
            raise forms.ValidationError(
                'questionnaire_url should not contain any space')
        if '　' in questionnaire_url:
            raise forms.ValidationError(
                'questionnaire_url should not contain any space')
        return questionnaire_url

    def save(self, post, file, user, commit=True):
        event = super(Create_Event_Form, self).save(commit=False)
        event.title = post["title"]
        event.detail = post["detail"]
        event.image = file["image"]
        event.detail = self.cleaned_data["detail"]
        event.user = user
        if commit:
            event.save()
        return event


class Change_UserInfo_Form(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['userid', 'email']
    error_message = 'error'
    userid = forms.CharField(required=True, label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '利用者IDを入力してください', 'class': 'form-control'}))
    email = forms.EmailField(max_length=255, label='EMAIL', required=True)
    is_save = False

    def clean_userid(self):
        userid = self.cleaned_data['userid']
        if ' ' in userid:
            raise forms.ValidationError('Userid should not contain any space')
        if '　' in userid:
            raise forms.ValidationError('Userid should not contain any space')
        return userid

    def clean_email(self):
        email = self.cleaned_data['email']
        if ' ' in email:
            raise forms.ValidationError('Email should not contain any space')
        if '　' in email:
            raise forms.ValidationError('Email should not contain any space')
        return email

    def save(self, post, user, commit=True):
        if user.userid == post["userid"]:
            user.userid = post["userid"]
        if user.userid == post["email"]:
            user.email = post["email"]
        if commit:
            user.save()
        return user


class Change_Shop_Form(forms.ModelForm):
    class Meta:
        model = Shop_Profile
        fields = ['name', 'icons', 'headers',
                  'online_address', 'self_introduction']
    name = forms.CharField(label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '名前を入力してください', 'class': 'form-control'}))
    icons = forms.ImageField(required=False)
    headers = forms.ImageField(required=False)
    error_message = 'error'
    online_address = forms.URLField()
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION',
                                        max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    is_save = False

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise forms.ValidationError('Name should not contain any space')
        if '　' in name:
            raise forms.ValidationError('Name should not contain any space')
        return name

    def clean_online_address(self):
        address = self.cleaned_data['online_address']
        if ' ' in address:
            raise forms.ValidationError(
                'OnlineAddress should not contain any space')
        if '　' in address:
            raise forms.ValidationError(
                'OnlineAddress should not contain any space')
        return address

    def save(self, post, file, user, profile, commit=True):
        profile.name = post["name"]
        if file:
            if 'icons' in file:
                profile.icons = file["icons"]
            if 'headers' in file:
                profile.headers = file["headers"]
        profile.self_introduction = post["self_introduction"]
        profile.online_address = post["online_address"]
        profile.shop = user
        if commit:
            profile.save()
        return profile


class Change_Cus_Form(forms.ModelForm):
    class Meta:
        model = Cus_Profile
        fields = ['name', 'icons', 'headers', 'gender', 'self_introduction']

    name = forms.CharField(label='NAME', max_length=30, widget=forms.TextInput(
        attrs={'placeholder': '名前を入力してください', 'class': 'form-control'}))
    icons = forms.ImageField(required=False)
    headers = forms.ImageField(required=False)
    error_message = 'error'
    GENDER = [('man', '男性'), ('woman', '女性'), ('No', '未回答')]
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION',
                                        max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    is_save = False

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise forms.ValidationError('Name should not contain any space')
        if '　' in name:
            raise forms.ValidationError('Name should not contain any space')
        return name

    def save(self, post, file, user, profile, commit=True):
        profile.name = post["name"]
        if file:
            if 'icons' in file:
                profile.icons = file["icons"]
            if 'headers' in file:
                profile.headers = file["headers"]
        profile.self_introduction = post["self_introduction"]
        profile.gender = post["gender"]
        profile.cus = user
        if commit:
            profile.save()
        return profile
