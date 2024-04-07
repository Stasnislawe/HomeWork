import random
from string import hexdigits

from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.mail import send_mail
from django.forms import Textarea
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Comment, Advert, User



# class SignupRegForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User


class RegistrationForm(SignupForm):
    # class Meta(SignupForm.Meta):
    #     model = User

    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user



class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ('heading', 'text', 'cat_name', 'n_files', 'n_photos')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comm_text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['comm_text'].widget = Textarea(attrs={'rows':5})