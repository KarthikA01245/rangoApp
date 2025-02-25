from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ['name']

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter the page title.")
    url = forms.URLField(max_length=200, help_text="Enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        fields = ['title', 'url', 'views']

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfile(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.FileField(required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


