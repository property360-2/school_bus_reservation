# reservations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse  # ADD THIS IMPORT
from .models import Reservation, UserProfile, Bus
from .forms import ReservationForm, UserRegistrationForm

def home(request):
    """Home page view"""
    buses_available = Bus.objects.exists()
    return render(request, 'home.html', {'buses_available': buses_available})

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type']
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def my_reservations(request):
    """View user's reservations"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate counts
    pending_count = reservations.filter(status='pending').count()
    confirmed_count = reservations.filter(status='confirmed').count()
    cancelled_count = reservations.filter(status='cancelled').count()
    
    context = {
        'reservations': reservations,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'total_count': reservations.count(),
    }
    
    return render(request, 'my_reservation.html', context)

@login_required
def make_reservation(request):
    """Make a new reservation"""
    buses = Bus.objects.all()
    
    if not buses.exists():
        messages.warning(request, 'No buses available. Please contact administrator.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.status = 'pending'  # Default status
            reservation.save()
            messages.success(request, '🎉 Reservation created successfully!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    
    return render(request, 'reservation_form.html', {
        'form': form,
        'buses': buses
    })

# Check if user is admin
def is_admin(user):
    try:
        return user.userprofile.user_type == 'admin'
    except:
        return user.is_staff  # Fallback to Django's is_staff

@user_passes_test(is_admin)
@login_required
def admin_reservations(request):
    """Admin view all reservations"""
    reservations = Reservation.objects.all().order_by('-created_at')
    
    # Counts for admin
    pending_count = reservations.filter(status='pending').count()
    confirmed_count = reservations.filter(status='confirmed').count()
    cancelled_count = reservations.filter(status='cancelled').count()
    
    context = {
        'reservations': reservations,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'total_count': reservations.count(),
    }
    
    return render(request, 'admin_reservation.html', context)

@user_passes_test(is_admin)
@login_required
def confirm_reservation(request, reservation_id):
    """Admin confirms a reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'confirmed'
    reservation.save()
    messages.success(request, f'Reservation #{reservation.id} confirmed successfully!')
    return redirect('admin_reservations')

@user_passes_test(is_admin)
@login_required
def reject_reservation(request, reservation_id):
    """Admin rejects a reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.status = 'cancelled'
    reservation.save()
    messages.warning(request, f'Reservation #{reservation.id} has been rejected.')
    return redirect('admin_reservations')

@login_required
def cancel_reservation(request, reservation_id):
    """User cancels their own reservation"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.status == 'pending':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reservation cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel a confirmed reservation.')
    
    return redirect('my_reservations')

def logout_view(request):
    """Custom logout view that accepts both GET and POST"""
    if request.method in ['GET', 'POST']:
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')
    
    # If neither GET nor POST, return error
    return HttpResponse("Method not allowed", status=405)