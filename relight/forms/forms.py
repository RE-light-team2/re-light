from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from relight.models import UserInfo

class Create_account_Form(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1','password2', 'email', 'icon','header','gender','s_or_c','self_introduction']

    password1 = forms.CharField(label='PASSWORD', max_length=128,widget=forms.PasswordInput(attrs={'placeholder':'パスワードを入力してください', 'class':'form-control', 'autocomplete' : 'off'}))
    password2 = forms.CharField(label='PASSWORDCONFIRM', max_length=128,widget=forms.PasswordInput(attrs={'placeholder':'パスワードを再度入力してください', 'class':'form-control', 'autocomplete' : 'off'}))
    icon = forms.ImageField()
    header = forms.ImageField()
    error_message = 'error'
    username = forms.CharField(label='USERNAME', max_length=30,widget=forms.TextInput(attrs={'placeholder':'名前を入力してください', 'class':'form-control'}))
    email = forms.CharField(label='EMAIL', max_length=30,widget=forms.TextInput(attrs={'placeholder':'emailを入力してください', 'class':'form-control', 'autocomplete': 'email'}))   
    GENDER=[('man','男'),('woman','女')]
    S_OR_C=[('shop','企業様'),('customer','一般様')]
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect())
    s_or_c = forms.ChoiceField(choices=S_OR_C, widget=forms.RadioSelect())
    self_introduction = forms.CharField(required=False, label='SELF_INTRODUCTION', max_length=1000,widget=forms.Textarea(attrs={'rows' : 5, 'class':'form-control'}))
    is_save = False
    
    def save(self, post):
        info = UserInfo()
        info.password = post['password1']
        info.email = post['email']
        info.icons = post['icon']
        info.headers = post['header']
        info.name = post['username']
        info.self_introduction = post['self_introduction']
        info.gender = post['gender']
        info.s_or_c = post['s_or_c']
        info.save()

        self.is_save = True