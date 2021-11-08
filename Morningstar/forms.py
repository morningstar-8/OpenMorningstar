from django import forms
from captcha.fields import ReCaptchaField
from django.core.validators import RegexValidator
from Morningstar.models import User
from .models import User

# widget, validators


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名", initial="", required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "小仙女"}))
    password = forms.CharField(
        label="密码", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "yyds"}), required=True)
    captcha = ReCaptchaField(label="人机验证")


class RegisterFormWithPhoneNumber(forms.Form):
    username = forms.CharField(
        label="Username", initial="admin", required=True)
    password = forms.CharField(
        label='重复密码', widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(), required=True)
    mobile_phone = forms.CharField(label='手机号',
                                   validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ], required=True)
    code = forms.CharField(
        label='验证码', widget=forms.TextInput(), required=True)
