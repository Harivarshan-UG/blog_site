from django.db import models
from django.utils.text import slugify


#category model

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#Author model 
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    avatar_url = models.URLField(blank=True, null=True, default='https://placehold.co/100x100/1F2937/FFFFFF?text=A')

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img_url = models.URLField(blank=True, null=True, default='https://placehold.co/600x400/1F2937/FFFFFF?text=Image')
    author_avatar_url = models.URLField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
   #Practice Code to display the title when object is printed
