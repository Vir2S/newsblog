from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image


class Post(models.Model):

    title = models.CharField('Title', max_length=150)
    content = models.TextField('Content')
    date_created = models.DateTimeField('Created', auto_now_add=True)
    date_posted = models.DateTimeField('Posted', default=timezone.now)
    date_updated = models.DateTimeField('Updated', auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField('Image', default='no_image.jpg', upload_to='post_pics')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def save(self):
        super().save()

        img = Image.open(self.post_image.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.post_image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Tag(models.Model):

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
