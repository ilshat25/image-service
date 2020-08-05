from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model

import urllib

class LocalUserSignupForm(SignupForm):
    
    def __init__(self, *args, **kwargs):
        super(LocalUserSignupForm, self).__init__(*args, **kwargs)
        self.fields['photo'] = forms.ImageField(required=False)

    def save(self, request):
        user = super(LocalUserSignupForm, self).save(request)
        user.photo = self.cleaned_data.get('photo')
        user.save()
        return user


class LocalUserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'photo']