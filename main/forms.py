from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import *

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class NewCategoryForm(forms.ModelForm):
    tutorial_category = forms.CharField(label='Category Name', required=True)
    category_summary = forms.CharField(label='Category Summary', required=True)
    category_slug = forms.CharField(label="Category Reference", required = False)

    class Meta:
        model = TutorialCategory
        fields = ("tutorial_category", "category_summary", "category_slug")

class NewSeriesForm(forms.ModelForm):
    tutorial_category = forms.ModelChoiceField(label="Category Reference", required=False, queryset = TutorialCategory.objects.all())
    class Meta:
        model = TutorialSeries
        fields = ("tutorial_series", "series_summary", "tutorial_category")

class NewTutorialForm(forms.ModelForm):
    tutorial_slug = forms.CharField(label='Tutorial Slug', required = False)
    tutorial_series = forms.ModelChoiceField(label="Series Reference", required=False, queryset = TutorialSeries.objects.all())
    tutorial_published = forms.DateTimeField(label="Published", required=False)

    class Media:
        js = ('/site_media/static/tiny_mce/tinymce.min.js',)

    class Meta:
        model = Tutorial
        fields = {"tutorial_title", "tutorial_content", "tutorial_published", "tutorial_series", "tutorial_slug"}

    field_order = ['tutorial_title', 'tutorial_content']
