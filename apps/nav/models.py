from django.db import models
from Morningstar.models import User


class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    excludeList = models.CharField(max_length=1000, blank=True, default='')

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name
