# Generated by Django 2.0.5 on 2018-06-05 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=250, verbose_name='作業名稱'),
        ),
    ]
