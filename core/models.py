from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = EmbedVideoField()
    summary = models.TextField()
    thumbnail_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.subject}"
