from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=200, blank=True, null=True, verbose_name='邮箱',)
    phone = models.CharField(
        unique=True, verbose_name="手机号", max_length=32, blank=True, null=True)
    bio = models.TextField(verbose_name="个人简介", blank=True, null=True)
    avatar = models.ImageField(
        verbose_name="头像", default="avatar.svg", blank=True, null=True)
    # USERNAME_FIELD = 'email'  # TODO: 可以改成 phone_number, email
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "档案"
        verbose_name_plural = verbose_name
