from cProfile import label
from pickle import TRUE
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField
from PIL import Image
# Create your models here

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=True)
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

    def save(self, *args,**kwargs):
        super().save(*args, **kwargs)
        try:
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