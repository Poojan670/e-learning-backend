# Generated by Django 3.2.9 on 2022-05-12 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_language', to='home.languages')),
            ],
        ),
        migrations.CreateModel(
            name='ExampleTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_popular', models.BooleanField(default=False)),
                ('example_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='example_title', to='examples.examplecategory')),
            ],
        ),
        migrations.CreateModel(
            name='ExamplesHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description1', models.TextField()),
                ('description2', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('language', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='examples_header', to='home.languages')),
            ],
        ),
        migrations.CreateModel(
            name='ExampleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='tutorials')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('relation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='example_detail', to='examples.exampletitle')),
            ],
        ),
    ]