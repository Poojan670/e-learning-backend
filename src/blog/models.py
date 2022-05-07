from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    title = models.CharField(max_length=100, null=False,
                             blank=False, help_text="Blog-Title")

    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class SubBlogs(models.Model):

    sub_title = models.CharField(
        max_length=100, null=True, blank=True, help_text="Blog-Sub Title")

    content = models.TextField()

    image = models.ImageField(upload_to="blogs")

    blog = models.ForeignKey(Blog, on_delete=models.PROTECT)

    def __str__(self):
        return self.sub_title
