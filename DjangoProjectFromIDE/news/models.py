from django.db import models

from djangopv35_v1 import settings


# Create your models here.
class News (models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='news', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    cover_image = models.ImageField(upload_to='news/cover_images/', blank=True, null=True)

    def __str__(self):
        return self.title