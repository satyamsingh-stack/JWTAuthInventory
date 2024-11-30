from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=255, unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)

class Inventory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.TextField()
    quantity=models.IntegerField(default=0)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    added_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='inv')