# Generated by Django 2.0.5 on 2018-06-05 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_work'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='filename',
        ),
        migrations.AddField(
            model_name='work',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='檔案'),
        ),
        migrations.AlterField(
            model_name='work',
            name='memo',
            field=models.TextField(default='', verbose_name='心得'),
        ),
    ]
