from django.db import models

# Create your models here.


class Crismastree(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='crismastree_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='crismastrees', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('auth.User', related_name='updated_crismastrees', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class CrismasTreeLike(models.Model):
    crismastree = models.ForeignKey(Crismastree, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True )