# Generated by Django 2.0.5 on 2018-06-06 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180605_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('q1', models.IntegerField(default=0)),
                ('q2', models.IntegerField(default=0)),
                ('q3', models.IntegerField(default=0)),
                ('t1', models.TextField(default='')),
                ('t2', models.TextField(default='')),
            ],
        ),
    ]
