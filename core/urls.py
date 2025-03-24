from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('videos/create/', views.video_create, name='video_create'),
    path('videos/<int:pk>/edit/', views.video_edit, name='video_edit'),
    path('videos/<int:pk>/delete/', views.video_delete, name='video_delete'),
    path('profile/', views.profile, name='profile'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/<int:pk>/delete/', views.delete_room, name='delete_room'),
    path('rooms/<int:pk>/edit/', views.edit_room, name='edit_room'),
]