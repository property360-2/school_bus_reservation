# reservations/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, UserProfile

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('driver', 'Driver'),
    )
    
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['bus', 'reservation_date', 'pickup_time', 'pickup_location', 'dropoff_location']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }