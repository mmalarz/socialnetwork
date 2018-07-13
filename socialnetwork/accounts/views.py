from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import RegistrationForm, EditProfileForm, ChangeImageForm
from accounts.models import UserProfile
from posts.models import Post


def profile(request, current_user):
    user = get_object_or_404(User, username=current_user)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': user_posts,
        'posts_count': len(user_posts)
    }
    return render(request, 'accounts/profile.html', context)


def settings(request, current_user):
    user = get_object_or_404(User, username=current_user)
    user_profile = get_object_or_404(UserProfile, user=user)

    if user == request.user:
        if request.method == 'POST':

            if 'email' in request.POST:
                form = EditProfileForm(request.POST, instance=request.user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile details updated.')
                else:
                    messages.error(request, 'Error: Profile details not updated.')
                return redirect('accounts:settings', current_user=request.user)

            elif 'new_password1' in request.POST:
                form = PasswordChangeForm(data=request.POST, user=request.user)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    messages.success(request, 'Password has been changed.')
                else:
                    messages.error(request, 'Error: Password has not been changed')
                return redirect('accounts:settings', current_user=request.user)

            elif 'image' in request.FILES:
                form = ChangeImageForm(request.POST, request.FILES, instance=user_profile)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Image has been changed')
                else:
                    messages.error(request, 'Error: Image has not been changed')
                return redirect('accounts:settings', current_user=request.user)

        else:
            user_form = EditProfileForm(instance=user)
            image_form = ChangeImageForm(instance=user_profile)
            password_form = PasswordChangeForm(user=request.user)
            context = {
                'user_form': user_form,
                'image_form': image_form,
                'password_form': password_form,
            }
            return render(request, 'accounts/settings.html', context)

    else:
        raise Http404


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('accounts:login')
    else:
        context = {
            'form': RegistrationForm(),
        }
        return render(request, 'accounts/registration.html', context)


def startpage(request):
    return render(request, 'accounts/start_page.html', {})
