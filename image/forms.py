from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

import requests

import urllib

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description','url')
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        print("----", extension)
        if not extension in valid_extensions:
            raise forms.ValidationError('The given URL does not mutch valid image extensions.')
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        print('------------', image_url)
        extension = image_url.rsplit('.', 1)[1].lower()
        name = slugify(image.title)
        image_name = f'{name}.{extension}'
        response = requests.get(image_url, stream=True)
        image.image.save(image_name,
                         ContentFile(response.raw.read()),
                         save=False)
        
        if commit:
            image.save()
        return image
