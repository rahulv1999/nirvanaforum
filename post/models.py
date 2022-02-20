from cProfile import label
from pickle import TRUE
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from tinymce import HTMLField
from PIL import Image
# Create your models here

User = get_user_model()

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=True)
    content  = HTMLField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id' : self.id
        })
    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id' : self.id
        })
    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id' : self.id
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    @property
    def like_count(self):
        return PostLike.objects.filter(post=self).count()

    

class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=True,null=False)
    
    def save(self, *args,**kwargs):
        super().save(*args, **kwargs)
        try:
            print(self.thumbnail)
            img = Image.open(self.thumbnail.path)
            if img.height>500 or img.weight>500:
                output_size = (500,500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)
        except:
            pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)

    def  __str__(self):
        return self.user.username