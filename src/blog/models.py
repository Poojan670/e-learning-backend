from django.db import models

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    title = models.CharField(max_length=100, null=False,
                             blank=False, help_text="Blog-Title")

    sub_title = models.CharField(
        max_length=100, null=True, blank=True, help_text="Blog-Sub Title")

    content = models.TextField()

    image = models.ImageField(upload_to="blogs")

    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title
