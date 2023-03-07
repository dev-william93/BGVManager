from django.db import models
import random
from django.contrib.auth.models import User
from django.utils import timezone


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class UserExtension(models.Model):
    
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    def create_new_ref_number():
      return str(random.randint(1000000000, 9999999999))[:6]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(default=timezone.now)
    father_name = models.CharField(max_length=150)
    gender = models.CharField(choices=gender_choice, default='male', max_length=10)
    reference = models.IntegerField(primary_key=True, default=create_new_ref_number, editable=False)