# Generated by Django 2.1.2 on 2020-10-06 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('s_or_c', models.CharField(max_length=2, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('gender', models.CharField(max_length=2, unique=True)),
                ('self_introduction', models.CharField(blank=True, max_length=500)),
                ('icons', models.ImageField(unique=True, upload_to='icons/', verbose_name='アイコン')),
                ('headers', models.ImageField(unique=True, upload_to='headers/', verbose_name='アイコン')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('detail', models.CharField(max_length=500)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
