from django.db import models
from core.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return str(self.name)
  

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.author} on {self.post}"
