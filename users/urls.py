from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('list/', views.list_view, name='list'),
    path('items/<int:pk>/', views.item_view, name='list-items'),
    path('friends/', views.manage_friends, name='friends'),
    path('friends/add_friend_request', views.add_friend_request, name='add-friend-request'),
    path('friends/remove_friend_request', views.remove_friend_request, name='friend-friend-request'),
]