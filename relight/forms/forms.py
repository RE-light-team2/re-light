from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,get_user_model
from relight.models import UserInfo , Event
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

class Create_Event_Form(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title","detail","questionnaire_url","image")

    image = forms.ImageField()
    title = forms.CharField(label='TITLE', max_length=256,widget=forms.TextInput(attrs={'placeholder':'タイトルを入力してください', 'class':'form-control'}))
    detail = forms.CharField(label='DETAIL',  max_length=1000, widget=forms.Textarea(attrs={'rows' : 5, 'class':'form-control'}))
    questionnaire_url = forms.CharField(label='URL', max_length=500,widget=forms.TextInput(attrs={'placeholder':'アンケート用のURLを入力してください', 'class':'form-control'}))

    def save(self,post,file,user):
        event = Event()
        event.title = post["title"]
        event.detail = post["detail"]
        event.image = file["image"]
        event.detail = self.cleaned_data["detail"]
        event.user = user
        event.save()