from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.core.files.base import ContentFile
from django.utils.text import slugify

import urllib

class LocalUserSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = DefaultSocialAccountAdapter.save_user(self, request, sociallogin, form)
        if not user.photo:
            socialacc = SocialAccount.objects.filter(user=user)[0]
            image_url = None
            print(socialacc.provider)
            if socialacc.provider == 'google':
                image_url = socialacc.extra_data['picture']
            elif socialacc.provider == 'vk':
                image_url = socialacc.extra_data['photo']
            
            if image_url:
                image_name = slugify(user.username) + '.' + image_url.rsplit('.', 1)[1].lower()
                print(image_name, image_url)
                # download the image from the given URL
                response = urllib.request.urlopen(image_url)
                user.photo.save(image_name,
                                ContentFile(response.read()))
        return user