from django.urls import path, include
from . import views
app_name = 'forum'
urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include('forum.api.urls')),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name="delete-message"),
    path('profile/<int:pk>/', views.userProfile, name='user-profile'),
    path('update-user/', views.updateUser, name="update-user"),
    path("topics/", views.topicsPage, name="topics"),
    path('activities/', views.activitiesPage, name="activities"),
]
