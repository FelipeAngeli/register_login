from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home_view, 
    login_view, 
    register_view, 
    update_profile_view, 
    activate_account
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('update-profile/', update_profile_view, name='update_profile'),
    path('activate/<str:email>/', activate_account, name='activate_account'),
    path('home/', home_view, name='home'), 
]