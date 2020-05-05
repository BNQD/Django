"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from . import views #From relative

app_name = "main"

urlpatterns = [
    path("", views.homepage, name = "homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("author/", views.author, name="author"),

    path('accounts/', include('django.contrib.auth.urls')),

    path("new_category/", views.new_category, name="new_category"),
    path("new_series/", views.new_series, name="new_series"),

    path("manage_account/", views.manage_account, name="manage_account"),
    path("change_password/", views.change_password, name="change_password"),

    path("<single_slug>", views.single_slug, name="single_slug"),


]
