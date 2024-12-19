from django.urls import include, path
from django.shortcuts import redirect

from django.contrib import admin
from accounts.views import update_profile_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('login')),
    path("accounts/", include("accounts.urls")),
    path("update-profile/", update_profile_view, name="update_profile"),
]
