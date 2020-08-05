from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/')

    def get_user_photo(self):
        return self.photo
    
    