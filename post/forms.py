from dataclasses import fields
from django import forms
from tinymce.widgets import TinyMCE
from .models import Post,Comment

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
