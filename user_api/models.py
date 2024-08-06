from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    dob = models.DateField()
    location = models.CharField(max_length=1200)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    bio = models.TextField()
    phone = models.BigIntegerField(unique=True)

    def __str__(self):
        return f'{self.user.username} - Profile'
