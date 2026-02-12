# reservations/admin.py
from django.contrib import admin
from .models import UserProfile, Bus, Reservation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone_number']
    list_filter = ['user_type']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'capacity', 'driver', 'current_location']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bus', 'reservation_date', 'pickup_time', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__username', 'bus__bus_number']