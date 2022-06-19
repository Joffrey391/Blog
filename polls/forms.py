from django import forms
from .models import Post

class Create_User_Form(forms.Form):
    nick = forms.CharField()
    about = forms.CharField()
    login = forms.CharField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'put_user_here', 'type': 'hidden'}),
            'contents': forms.Textarea(attrs={'class': 'form-control'}),
            'limit': forms.Select(choices=Post.LIMITS, attrs={'class': 'form-control'}),
        }

class Post_Update_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'password', 'limit', 'contents', 'image')

        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'contents': forms.Textarea(attrs={'class': 'form-control'}),
            'limit': forms.Select(choices=Post.LIMITS, attrs={'class': 'form-control'}),
        }

class Comment_Form(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'value':'50', 'id':'elder', 'type': 'hidden'}))

class Password_Post_Form(forms.Form):
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))