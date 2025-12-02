from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterForm, PinForm, DiaryEntryForm
from .models import DiaryProfile, DiaryEntry

# -------- Registration --------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # create diary profile
            DiaryProfile.objects.create(user=user)

            messages.success(request, "Account created. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'diary_app/register.html', {'form': form})


# -------- Login / Logout --------
from django.contrib.auth import views as auth_views

# Use Django's auth_views.LoginView / LogoutView in urls.py for simplicity


# -------- Set / Change PIN --------
@login_required
def set_pin_view(request):
    profile, _ = DiaryProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            profile.set_pin(pin)
            profile.save()
            messages.success(request, "Diary PIN set successfully.")
            return redirect('unlock_diary')
    else:
        form = PinForm()

    return render(request, 'diary_app/set_pin.html', {'form': form})


# -------- Unlock Diary --------
@login_required
def unlock_diary_view(request):
    profile, _ = DiaryProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            if profile.check_pin(pin):
                request.session['diary_unlocked'] = True
                return redirect('diary_home')
            else:
                request.session['diary_unlocked'] = False
                messages.error(request, "Incorrect PIN.")
    else:
        form = PinForm()

    return render(request, 'diary_app/unlock.html', {'form': form})



def diary_unlocked_required(view_func):
    def _wrapped(request, *args, **kwargs):
        # Not logged in → go to login
        if not request.user.is_authenticated:
            return redirect('login')

        # Session missing or false → force unlock page
        if request.session.get('diary_unlocked') != True:
            return redirect('unlock_diary')

        return view_func(request, *args, **kwargs)
    return _wrapped


# -------- Diary pages --------
@login_required
@diary_unlocked_required
def diary_home_view(request):
    entries = DiaryEntry.objects.filter(user=request.user)
    return render(request, 'diary_app/diary_home.html', {'entries': entries})


@login_required
@diary_unlocked_required
def diary_new_view(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('diary_home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary_app/diary_new.html', {'form': form})


@login_required
@diary_unlocked_required
def diary_detail_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    return render(request, 'diary_app/diary_detail.html', {'entry': entry})

def logout_view(request):
    logout(request)
    request.session.flush()  # Clears diary_unlocked safely
    return redirect('login')