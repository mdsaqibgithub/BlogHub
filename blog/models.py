from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True) 
    tags = models.CharField(max_length=100, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)


    def total_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return f"Comment by {self.user.username} on {self.blog.title}"