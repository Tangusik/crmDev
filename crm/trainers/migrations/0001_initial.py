# Generated by Django 3.2.19 on 2023-07-31 20:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='имя абонемента', max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('duration', models.DurationField(null=True)),
                ('lesson_count', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adres', models.CharField(blank=True, default='Адрес площадки', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='qwerty', max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('reg_date', models.DateField(auto_now=True)),
                ('birth_date', models.DateField(blank=True, default=datetime.date(2023, 1, 1))),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('expiry_date', models.DateTimeField(verbose_name='expiry date')),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='SportType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Спорт', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('otchestv', models.CharField(blank=True, max_length=20)),
                ('birthdate', models.DateField()),
                ('status', models.CharField(default='Тренер', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('clients', models.ManyToManyField(to='trainers.Client')),
                ('sport_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainers.sporttype')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainers.trainer')),
            ],
        ),
        migrations.AddField(
            model_name='sporttype',
            name='trainers',
            field=models.ManyToManyField(to='trainers.Trainer'),
        ),
        migrations.CreateModel(
            name='PurchaseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_end', models.DateField(null=True)),
                ('activitys_left', models.IntegerField(null=True)),
                ('abonement', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trainers.abonement')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trainers.client')),
            ],
        ),
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('email', models.CharField(blank=True, max_length=30)),
                ('telephone', models.CharField(blank=True, max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.client')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='123', max_length=30)),
                ('street', models.CharField(default='123', max_length=30)),
                ('house', models.CharField(blank=True, max_length=30)),
                ('building', models.CharField(blank=True, max_length=30)),
                ('flat', models.CharField(blank=True, max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainers.client')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_date', models.DateField()),
                ('act_time_begin', models.TimeField()),
                ('act_time_end', models.TimeField()),
                ('status', models.CharField(default='Состоится', max_length=20)),
                ('area', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='trainers.area')),
                ('clients', models.ManyToManyField(to='trainers.Client')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trainers.trainer')),
            ],
        ),
        migrations.AddField(
            model_name='abonement',
            name='clients',
            field=models.ManyToManyField(through='trainers.PurchaseHistory', to='trainers.Client'),
        ),
    ]
