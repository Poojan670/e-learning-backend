from django.contrib import admin
from .models import (
    InstructorProfile, Category, Course,
    VideoSections, VideoCourses, Overview,
    CourseNumbers, Certificates
)

admin.site.register(InstructorProfile)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(VideoSections)
admin.site.register(VideoCourses)
admin.site.register(Overview)
admin.site.register(CourseNumbers)
admin.site.register(Certificates)
