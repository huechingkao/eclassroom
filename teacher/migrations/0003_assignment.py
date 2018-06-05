# Generated by Django 2.0.5 on 2018-06-05 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_auto_20180603_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('classroom_id', models.IntegerField(default=0)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
