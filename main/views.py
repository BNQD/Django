from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tutorial, TutorialSeries, TutorialCategory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Q

import datetime
# Create your views here.
def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": TutorialCategory.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, "{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def author(request):
    return render(request=request,
                  template_name="main/author.html")

def manage_account(request):
    return render(request=request,
                  template_name="main/manage_account.html")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('main:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request = request,
                    template_name = "main/change_password.html",
                    context={"form":form})

def new_category(request):
    if request.method == 'POST':
        form = NewCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.category_slug = form.cleaned_data.get('tutorial_category')
            category.save()

            messages.success(request, 'New category created!')
            return redirect(request.GET.get('prev'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NewCategoryForm()
        form.fields['category_slug'].widget = forms.HiddenInput()
    return render(request, "main/new_category.html", {"form": form})

def new_series(request):
    if request.method == 'POST':
        form = NewSeriesForm(request.POST)
        if form.is_valid():
            series = form.save(commit=False)
            series.tutorial_category = TutorialCategory.objects.filter(tutorial_category=request.GET.get('prev').strip('/')).first()
            series.save()

            messages.success(request, 'New series created! ')
            return redirect(request.GET.get('prev'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NewSeriesForm()
        form.fields['tutorial_category'].widget = forms.HiddenInput()
    return render(request, "main/new_series.html", {"form": form})

def new_tutorial(request):
    if request.method == 'POST':
        form = NewTutorialForm(request.POST)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.tutorial_slug = form.cleaned_data.get('tutorial_title')
            tutorial.tutorial_series = TutorialCategory.objects.filter(tutorial_series=request.GET.get('prev').strip('/')).first()
            tutorial.tutorial_published = datetime.now()
            tutorial.save()

            messages.success(request, 'New series created! ')
            return redirect(request.GET.get('prev'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NewTutorialForm()
        form.fields['tutorial_slug'].widget = forms.HiddenInput()
        form.fields['tutorial_series'].widget = forms.HiddenInput()
        form.fields['tutorial_published'].widget = forms.HiddenInput()
    return render(request, "main/new_series.html", {"form": form})



def single_slug(request, single_slug):
    # first check to see if the url is in categories.
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]

    if single_slug in categories:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            try:
                part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
                series_urls[m] = part_one.tutorial_slug
            except:
                series_urls[m] = m.tutorial_series
        return render(request=request,
                      template_name='main/series.html',
                      context={"tutorial_series": matching_series, "part_ones": series_urls})



    elif single_slug in tutorials:
        this_tutorial = {}

        try:
            this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug)
            tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by('tutorial_published')
            this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)
            return render(request=request,
                          template_name='main/tutorial.html',
                          context={"tutorial": this_tutorial,
                                   "sidebar": tutorials_from_series,
                                   "this_tut_idx": this_tutorial_idx})
        except:
            pass

    else:
        return render(request=request,
                      template_name='main/tutorial.html',
                      context={"tutorial": {}},
                      )

