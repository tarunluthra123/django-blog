from django.db import models
from utils.codec import codec

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    bio = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = codec.encrypt(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
