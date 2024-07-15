from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from users.forms.profile_form import ProfileForm
from users.forms.login import LoginForm
from users.forms.register_form import RegisterForm
from ..models import Profile


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'pages/register_view.html',
        context={
            'form': form,
            'form_action': reverse('users:register_create'),
    })
    
    
def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user has been registered.')
        
        del(request.session['register_form_data'])
        return redirect('users:login')
    
    return redirect('users:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'pages/login.html',
        context={
            'form': form,
            'form_action': reverse('users:login_create')
    })
    
    
def login_create(request):
    if request.method != 'POST':
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)
            return redirect(reverse('users:dashboard'))
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        messages.error(request, 'Invalid username or password.')

    return redirect(reverse('users:login'))


@login_required(login_url='users:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('users:login'))
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('users:login'))
    
    logout(request)
    messages.success(request, 'Logged out successfully')
    
    return redirect(reverse('users:login'))
    

@require_http_methods(["GET", "POST"])
@login_required(login_url='users:login', redirect_field_name='next')
def ProfileView(request, id):
    profile = get_object_or_404(Profile, pk=id)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(reverse('users:profile', kwargs={'id': id}))
        else:
            messages.error(request, 'Error updating profile. Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'pages/profile.html', context)
