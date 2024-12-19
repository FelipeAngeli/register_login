from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import home_view, login_view, register_view, update_profile_view, activate_account
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('update-profile/', update_profile_view, name='update_profile'),
    path("activate/<str:email>/", activate_account, name="activate_account"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
if settings.DEBUG:  # Apenas no modo de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)