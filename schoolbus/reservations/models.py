# reservations/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = (
        ('admin', 'Administrator'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('driver', 'Driver'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

class Bus(models.Model):
    bus_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    driver = models.CharField(max_length=100)
    current_location = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Bus {self.bus_number}"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    pickup_time = models.TimeField()
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username}"