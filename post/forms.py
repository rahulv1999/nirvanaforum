from dataclasses import fields
from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from .models import Post,Comment, Account
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
class UserCreateForm(UserCreationForm):
    gender = forms.ChoiceField(choices=[('MALE', 'MALE'), ('FEMALE','FEMALE')],required=True)
    twitter_Username = forms.CharField(max_length=100,required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "gender","twitter_Username","email", "password1", "password2","profile_picture")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.gender = self.cleaned_data["gender"]
        user.twitter_Username = self.cleaned_data["twitter_Username"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        if commit:
            user.save()
        return user

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self,*args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 10}))

    class Meta:
        model = Post
        fields = ('title','content','categories')

class CommentForm(forms.ModelForm):
    content = forms.CharField(label=False,widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'placeholder' : 'Type your comment',
        'id' : 'usercomment',
        'rows': 3,
        'cols': 60,

    }))
    class Meta:
        model = Comment
        fields = ('content',)


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[('MALE', 'MALE'), ('FEMALE','FEMALE')],required=True)
    twitter_Username = forms.CharField(max_length=100,required=False)
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = Account
        fields = ("gender","twitter_Username","profile_picture")

    def save(self, commit=True):
        user = super(ProfileUpdateForm, self).save(commit=False)
        user.gender = self.cleaned_data["gender"]
        user.twitter_Username = self.cleaned_data["twitter_Username"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        try:
            img = Image.open(user.profile_picture.path)
            if img.height>500 or img.weight>500:
                output_size = (200,200)
                img.thumbnail(output_size)
                img.save(user.profile_picture.path)
        except:
            pass
        if commit:
            user.save()
        return user

