from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, get_user_model


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
