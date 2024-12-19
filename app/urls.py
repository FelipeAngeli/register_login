from django.urls import include, path
from django.shortcuts import redirect
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import activate_account


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),
    path('accounts/', include('accounts.urls')),
    path('activate/<str:email>/', activate_account, name='activate_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)