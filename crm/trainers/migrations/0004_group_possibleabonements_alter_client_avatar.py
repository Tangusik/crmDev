# Generated by Django 4.2.7 on 2024-03-18 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0003_alter_client_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='possibleAbonements',
            field=models.ManyToManyField(to='trainers.abonement'),
        ),
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(upload_to='avatars'),
        ),
    ]