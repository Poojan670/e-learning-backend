# Generated by Django 3.2.9 on 2022-05-12 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Blog-Title', max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SubBlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_title', models.CharField(blank=True, help_text='Blog-Sub Title', max_length=100, null=True)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='blogs')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.blog')),
            ],
        ),
    ]
