# Generated by Django 3.2.9 on 2022-05-12 13:53

import cloudinary_storage.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import src.courses.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('icon', models.ImageField(blank=True, upload_to=src.courses.models.category_image_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(help_text='Certificate File for the course', null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=src.courses.models.certificate_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['docs', 'pdf'])])),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('comment_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250, unique=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, upload_to=src.courses.models.product_image_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('views', models.IntegerField(default=0, help_text='total no of views for this course')),
                ('ratings', models.DecimalField(decimal_places=1, default=0, help_text='Overall Review Score for the course!', max_digits=5)),
                ('reviews_no', models.IntegerField(default=0, help_text='Overall no of reviews')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.CharField(choices=[('B', 'Beginning Level'), ('M', 'Mid-Level'), ('A', 'Advanced Level'), ('S', 'Senior Level')], help_text='Skill Level of the course B-Beginner, M-Mid Level, A-Advanced Level, S-Senior Level', max_length=1, verbose_name='Skill Level')),
                ('students', models.IntegerField(default=0, help_text='No of students that bought or applied for the course!')),
                ('languages', models.CharField(blank=True, default='English', help_text='Language that the entirerty of course is set on!', max_length=50, null=True, verbose_name='Course Language')),
                ('captions', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], help_text='Turn on captions or not', max_length=1)),
                ('lectures', models.IntegerField(blank=True, help_text='total no of lectures in the course!', null=True)),
                ('video_length', models.IntegerField(default=0, help_text='Total length of the course videos')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(help_text="Instructor's Profession", max_length=50)),
                ('about_me', models.TextField(help_text='Brief Description about the Instructor/User')),
                ('website', models.URLField(blank=True, help_text="Instructor's professional or personal website", null=True)),
                ('youtube', models.URLField(blank=True, help_text="Instructor's Youtube channel Link", null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Overview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='About this course', max_length=100, verbose_name='Title')),
                ('subtitle', models.CharField(help_text='1 to 2 lines about the course', max_length=255, verbose_name='Sub Title')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('reply_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('body', models.TextField(help_text='Review Description')),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('reviewed_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoSections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(help_text='Section Content for videos to be placed on, Eg: Section 1: Short Tutorials', max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.course')),
                ('video_ref', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.videosections')),
            ],
            options={
                'verbose_name': 'Video Section',
                'verbose_name_plural': 'Video Sections',
            },
        ),
        migrations.CreateModel(
            name='VideoCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(help_text="Title for the video, eg:'What will you learn?'", max_length=255)),
                ('video', models.FileField(help_text='Video File for the course', null=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(), upload_to=src.courses.models.courses_video_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.videosections')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewsReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('reply_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.reviews')),
            ],
        ),
    ]
