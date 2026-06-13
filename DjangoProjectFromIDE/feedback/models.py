from django.db import models

from djangopv35_v1 import settings


# Create your models here.
class Feedback(models.Model):
    fullName = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')

    answer_at = models.DateTimeField(auto_now=True)
    answer_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='answered_feedbacks')
    answer = models.TextField(blank=True)


    def __str__(self):
        return f"Feedback from {self.fullName} ({self.email}) at {self.created_at}"
