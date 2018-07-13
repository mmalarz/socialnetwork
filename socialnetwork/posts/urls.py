from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('add/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('edit/(<slug:slug>/', views.PostEditView.as_view(), name='post_edit'),
    path('remove/(<slug:slug>/', views.post_delete, name='post_delete'),

    path('<slug:post_slug>/remove-comment/<int:id>/', views.comment_delete, name='comment_delete'),
    path('<slug:post_slug>/edit-comment/<int:id>/', views.comment_edit, name='comment_edit'),
]
