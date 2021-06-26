from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import News


class AddCommentForm(forms.Form):
    username = forms.CharField(show_hidden_initial=False)
    comment_text = forms.CharField()


class AddNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title_news', 'content', 'tag']


class ExtendedRegisterForm(UserCreationForm):
    first_name = forms.CharField(min_length=3, required=False, help_text='Имя')
    last_name = forms.CharField(min_length=3, required=False, help_text='Фамилия')
    city = forms.CharField(max_length=36, required=False, help_text='город')
    phone_number = forms.CharField(max_length=11, required=False, help_text='номер телефона')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'city', 'phone_number')