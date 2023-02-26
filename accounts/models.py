from django.db import models
import random
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class UserExtension(models.Model):
    def create_new_ref_number():
      return str(random.randint(1000000000, 9999999999))[:6]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    father_name = models.CharField(max_length=150)
    reference = models.IntegerField(primary_key=True, default=create_new_ref_number, editable=False)