from django.urls import include, path
from django.shortcuts import redirect

from accounts import admin
from login_register.views import update_profile_view


urlpatterns = [
    path('', lambda request: redirect('login')),
    path("admin/", admin.site.urls),
    path("login_register/", include("login_register.urls")),
    path("update-profile/", update_profile_view, name="update_profile"),
]
