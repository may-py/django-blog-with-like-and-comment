from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image',null=True,blank=True)
    likes = models.ManyToManyField(User,related_name='post_likes')

    def __str__(self) -> str:
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('posts:post-detail',kwargs={'pk':self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User,on_delete=models.CASCADE) 
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return (f'{self.post.title} by {self.name}')