# reservations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # DAPAT NASA DITO ANG HOME!
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('make-reservation/', views.make_reservation, name='make_reservation'),
    path('register/', views.register, name='register'),
    path('admin-reservations/', views.admin_reservations, name='admin_reservations'),
    path('reservations/confirm/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('reservations/reject/<int:reservation_id>/', views.reject_reservation, name='reject_reservation'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/logout/', views.logout_view, name='accounts_logout'),
]