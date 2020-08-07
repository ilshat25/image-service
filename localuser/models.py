from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/')
    following = models.ManyToManyField('self',
                                       through='Contact',related_name='followers',
                                       symmetrical=False)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk, 'username': self.username, })
    

    def get_user_photo(self):
        return self.photo
 
    
class Contact(models.Model):
    user_from = models.ForeignKey(get_user_model(),
                                 related_name='rel_from_set',
                                 on_delete=models.CASCADE)
    user_to = models.ForeignKey(get_user_model(),
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'