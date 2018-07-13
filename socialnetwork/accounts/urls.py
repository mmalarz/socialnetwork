from django.contrib.auth.views import logout, LoginView
from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout, {'template_name': 'accounts/start_page.html'}, name='logout'),
    path('registration/', views.registration, name='registration'),

    path('profile/<str:current_user>/', views.profile, name='profile'),
    path('settings/<str:current_user>/', views.settings, name='settings'),
]
