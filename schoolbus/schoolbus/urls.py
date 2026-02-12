# schoolbus/urls.py (main urls file)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
    path('', include('reservations.urls')),  # INCLUDE RESERVATIONS APP
]

# O kung nasa reservations/urls.py ang home: