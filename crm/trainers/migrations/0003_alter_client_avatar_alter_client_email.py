# Generated by Django 4.2.7 on 2024-04-26 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0002_client_email_client_phone_trainer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(default='', height_field=300, upload_to='avatars', width_field=300),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]