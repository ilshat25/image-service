from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse

class Image(models.Model):
    publisher = models.ForeignKey(to=get_user_model(),
                                  related_name='images_created',
                                  on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="img/%Y/%m/%d/")
    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    users_like = models.ManyToManyField(get_user_model(),
                                        related_name='images_liked',
                                        blank=True)
    # total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', 
                        args=[self.pk, self.slug])

    def __str__(self):
        return self.title