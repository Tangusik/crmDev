# Generated by Django 4.2.5 on 2023-10-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0002_presence'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]