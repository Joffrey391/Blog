from django.conf import settings

from django.db import models
from django.urls import reverse

class Post(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=100)
    PUBLIC = 'P'
    PRIVATE = 'Pr'
    HIDDEN = 'H'
    LIMITS = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (HIDDEN, 'Hidden'),
    ]
    limit = models.CharField(
        max_length=2,
        choices=LIMITS,
        default=PUBLIC,
    )
    contents = models.TextField()
    image = models.ImageField(upload_to="pictures", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.user}, {self.id}"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})

    def delete(self, *args, **kwargs): #check this
        self.image.delete()
        super().delete(*args, **kwargs)

class Comment(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    contents = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title}, {self.user}, {self.id}"