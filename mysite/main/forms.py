from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import TutorialCategory

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
    category_slug = forms.CharField(label="Category Reference", required = True)

    class Meta:
        model = TutorialCategory
        fields = ("tutorial_category", "category_summary", "category_slug")





