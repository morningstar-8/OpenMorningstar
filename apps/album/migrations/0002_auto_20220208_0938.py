# Generated by Django 3.2.9 on 2022-02-08 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='foreignUrl',
            field=models.URLField(blank=True, verbose_name='外部图片链接'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, upload_to='photo/%Y%m%d%H/', verbose_name='本站托管图片'),
        ),
    ]
