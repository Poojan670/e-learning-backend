from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.core.validators import MaxValueValidator, MinValueValidator

import sys
sys.setrecursionlimit(1500)

User = get_user_model()


def category_image_path(instance, filename):
    return "category/icons/{}/{}".format(instance.name, filename)


def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)


def courses_video_path(instance, filename):
    return "courses/videos/{}/{}".format(instance.video_title, filename)


def certificate_file_path(instance, filename):
    return "courses/certificates/{}/{}".format(instance.course.title, filename)


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profession = models.CharField(
        max_length=50, help_text="Instructor's Profession")
    about_me = models.TextField(
        help_text="Brief Description about the Instructor/User")
    website = models.URLField(
        blank=True, null=True, help_text="Instructor's professional or personal website")
    youtube = models.URLField(blank=True, null=True,
                              help_text="Instructor's Youtube channel Link")

    def __str__(self):
        return self.user.full_name

    @property
    def get_user_mail(self):
        return self.user.emai


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Course(models.Model):

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    seller = models.ForeignKey(
        InstructorProfile, related_name="instructor", on_delete=models.PROTECT
    )

    category = TreeForeignKey(
        Category, related_name="course_category", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=250, unique=True, blank=False)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True)
    description = models.TextField(null=True, blank=True)
    views = models.IntegerField(
        default=0, help_text='total no of views for this course')

    ratings = models.DecimalField(
        default=0, decimal_places=1, max_digits=5, help_text='Overall Review Score for the course!')

    reviews_no = models.IntegerField(
        default=0, help_text="Overall no of reviews")

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class VideoSections(models.Model):
    section_no = models.IntegerField(default=1)
    section_title = models.CharField(
        max_length=255, help_text='Section Content for videos to be placed on, Eg: Section 1: Short Tutorials')

    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    video_ref = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.section_title

    @property
    def section_no(self):
        return self.section_no

    class Meta:
        verbose_name = _('Video Section')
        verbose_name_plural = _('Video Sections')


class VideoCourses(models.Model):
    video_title = models.CharField(
        max_length=255, help_text="Title for the video, eg:'What will you learn?'")
    video = models.FileField(upload_to=courses_video_path, null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], help_text='Video File for the course',
                             storage=VideoMediaCloudinaryStorage())
    date_uploaded = models.DateTimeField(auto_now_add=True)

    section = models.ForeignKey(VideoSections, on_delete=models.CASCADE)

    def __str__(self):
        return self.video_title


class Overview(models.Model):
    verbose_name = 'overview'
    verbose_name_plural = 'overviews'

    title = models.CharField(_('Title'), max_length=100,
                             help_text='About this course')
    subtitle = models.CharField(_('Sub Title'),
                                max_length=255, help_text='1 to 2 lines about the course')

    course = models.OneToOneField(Course, on_delete=models.PROTECT)

    def __str__(self):
        return f"Overview of Course:{self.course.title}"


class CourseNumbers(models.Model):

    skill_level_choices = (
        ('B', 'Beginning Level'),
        ('M', 'Mid-Level'),
        ('A', 'Advanced Level'),
        ('S', 'Senior Level'),
    )
    skill_level = models.CharField(
        _('Skill Level'), choices=skill_level_choices, max_length=1, help_text='Skill Level of the course B-Beginner, M-Mid Level, A-Advanced Level, S-Senior Level')
    students = models.IntegerField(
        default=0, help_text='No of students that bought or applied for the course!')
    languages = models.CharField(_('Course Language'), max_length=50, null=True, blank=True, default='English',
                                 help_text="Language that the entirerty of course is set on!")
    captions_choices = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    captions = models.CharField(
        choices=captions_choices, max_length=1, help_text='Turn on captions or not')
    lectures = models.IntegerField(
        blank=True, null=True, help_text="total no of lectures in the course!")
    video_length = models.IntegerField(
        default=0, help_text='Total length of the course videos')

    overview = models.OneToOneField(Overview, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill_level


class Certificates(models.Model):
    certificate = models.FileField(upload_to=certificate_file_path, null=True,
                                   validators=[FileExtensionValidator(
                                       allowed_extensions=['docs', 'pdf'],)],
                                   help_text='Certificate File for the course',
                                   storage=RawMediaCloudinaryStorage())
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class Comment(models.Model):
    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'

    comment_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    body = models.CharField(max_length=200)
    comment_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return "Comment : {} {}".format(self.user.full_name, self.course.title)


class Reply(models.Model):

    verbose_name = _('Reply')
    verbose_name_plural = _('Replies')
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    reply_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reply by {self.user.full_name}"


class Reviews(models.Model):

    review_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name='self_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)]
                                 )
    body = models.TextField(help_text="Review Description")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    reviewed_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Review: {} {}".format(self.user.full_name, self.course.title)


class ReviewsReply(models.Model):
    review = models.ForeignKey(
        Reviews, blank=True, null=True, on_delete=models.CASCADE, related_name='reviews')
    body = models.CharField(max_length=200)
    reply_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reply by {self.user.full_name}"


class Announcement(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"Announcement for {self.course.title} : {self.title}"
