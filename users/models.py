from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username=models.EmailField(unique=True,null=True)
    name=models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    password=models.CharField(max_length=200)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]


# Create your models here.
