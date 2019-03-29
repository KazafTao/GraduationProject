from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class LoginForm(forms.Form):
    user = forms.CharField(label=_(u"昵称"),
                           max_length=30,
                           widget=forms.TextInput(attrs={'size': 40, 'autocomplete': 'off'}))
    password = forms.CharField(label=_(u"密码"),
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"size": 40, 'autocomplete': 'off'}))


class RegisterForm(LoginForm):
    email = forms.EmailField(label=_(u"邮件"),
                             max_length=40,
                             widget=forms.TextInput(attrs={"size": 40, 'autocomplete': 'off'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'该邮件地址已注册.')
        return email
