from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,get_user_model
from relight.models import UserInfo
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


print(get_user_model())
class Create_account_Form(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'password1','password2', 'email', 'icons','headers','gender','s_or_c','self_introduction']

    password1 = forms.CharField(label='PASSWORD', max_length=128,widget=forms.PasswordInput(attrs={'placeholder':'パスワードを入力してください', 'class':'form-control', 'autocomplete' : 'off'}))
    password2 = forms.CharField(label='PASSWORDCONFIRM', max_length=128,widget=forms.PasswordInput(attrs={'placeholder':'パスワードを再度入力してください', 'class':'form-control', 'autocomplete' : 'off'}))
    icons = forms.ImageField()
    headers = forms.ImageField()
    error_message = 'error'
    name = forms.CharField(label='NAME', max_length=30,widget=forms.TextInput(attrs={'placeholder':'名前を入力してください', 'class':'form-control'}))
    email = forms.EmailField(max_length=255,label='EMAIL', required=True)   
    GENDER=[('man','男'),('woman','女')]
    S_OR_C=[('shop','企業様'),('customer','一般様')]
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    s_or_c = forms.ChoiceField(choices=S_OR_C, widget=forms.RadioSelect())
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION', max_length=1000,widget=forms.Textarea(attrs={'rows' : 5, 'class':'form-control'}))
    is_save = False
    
    def save(self, commit=True):
    # Call save of the super of your own class,
    # which is UserCreationForm.save() which calls user.set_password()
        user = UserInfo()
    # Add the things your super doesn't do for you
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.s_or_c = self.cleaned_data['s_or_c']
        user.gender = self.cleaned_data['gender']
        user.self_introduction = self.cleaned_data['self_introduction']
        user.icons = self.cleaned_data['icons']
        user.headers = self.cleaned_data['headers']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

    email = forms.EmailField(max_length=255,label='EMAIL', required=True)   
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs) 
        self.fields.pop('username') 
        for field in self.fields.values():
            print(field.widget)   
            field.widget.attrs['placeholder'] = field.label  