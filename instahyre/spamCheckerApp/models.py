from ssl import create_default_context
from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    uuid = models.UUIDField(primary_key= True , default = uuid.uuid4 , editable=False)
    name = models.CharField(null=False , max_length=30)
    username = models.CharField(null=False , max_length=30)
    email = models.EmailField(max_length=20 , null=True ,unique=True )
    phone = models.CharField(null=False , max_length=13 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class globalDB(models.Model):
    # uuid = models.UUIDField(primary_key= True , default = uuid.uuid4 , editable=False)
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE , null = False)
    spam_likelyhood = models.DecimalField(max_digits = 3 , decimal_places=2 ,default=0)
    n_spam = models.IntegerField(default=0 , null=False)
    is_registered = models.BooleanField(default=False , null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
