# Generated by Django 3.2.9 on 2022-05-12 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import src.user.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(help_text='Please enter your email address..', max_length=254, unique=True, verbose_name='email address')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('NaN', 'Rather not say')], default='NaN', max_length=3)),
                ('full_name', models.CharField(help_text='Please enter your full nmae', max_length=60, null=True, verbose_name='Full Name')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_verified')),
                ('otp', models.IntegerField(blank=True, null=True)),
                ('activation_key', models.CharField(blank=True, max_length=150, null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to=src.user.models.user_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='DeactivateUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deactive', models.BooleanField(default=True)),
                ('deactivated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deactivate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]