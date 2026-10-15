from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import SignupForm, ProfileForm
from .models import Profile


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'auth.html', {'form': form, 'signup': False})


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    data = request.POST.copy() if request.method == 'POST' else None
    if data is not None and 'password' in data:
        data['password1'] = data.get('password')
        data['password2'] = data.get('confirm-password')
    form = SignupForm(data)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'auth.html', {'form': form, 'signup': True})

@login_required
@require_POST
def log_out(request):
    logout(request)
    return redirect('signin')

@login_required
def profile(request, username):
    person = get_object_or_404(User, username=username)
    details, _ = Profile.objects.get_or_create(user=person)
    mine, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'person': person, 'details': details,
        'is_following': mine.following.filter(pk=details.pk).exists(),
        'posts': person.post_set.select_related('user').order_by('-created_at')})

@login_required
def edit_profile(request):
    details, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST if request.method == 'POST' else None, instance=details)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile', username=request.user.username)
    return render(request, 'form.html', {'form': form, 'heading': 'Edit your profile'})

@login_required
@require_POST
def follow(request, username):
    person = get_object_or_404(User, username=username)
    if person != request.user:
        mine, _ = Profile.objects.get_or_create(user=request.user)
        other, _ = Profile.objects.get_or_create(user=person)
        if mine.following.filter(pk=other.pk).exists():
            mine.following.remove(other)
        else:
            mine.following.add(other)
    return redirect('profile', username=username)

@login_required
def network(request):
    mine, _ = Profile.objects.get_or_create(user=request.user)
    people = User.objects.exclude(pk=request.user.pk).select_related('profile').order_by('username')
    q = request.GET.get('q', '').strip()
    if q:
        people = people.filter(username__icontains=q)
    return render(request, 'network.html', {'people': people, 'following_ids': list(mine.following.values_list('user_id', flat=True)), 'q': q})
