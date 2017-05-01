from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    content = models.TextField(blank=False)
    author = models.ManyToManyField('BlogUser', related_name='posts')
    tag = models.ManyToManyField(Tag, related_name='posts') # връща обратно от инстанция на ТАГ постовете свързани с него
    comment = models.ForeignKey('Comment', related_name='posts', null=True)

class BlogUser(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str('{}'.format(self.email))

class Comment(models.Model):
    author = models.ManyToManyField(BlogUser)
    created_at = models.DateField(default=timezone.now)
    content = models.TextField(blank=False)
    post = models.ForeignKey('BlogPost',related_name='comments', null=True)
