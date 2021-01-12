from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from accounts.api import UserModelViewSet, FriendListViewSet
from . import views


# app_name = "accounts"
router = DefaultRouter()
router.register(r'user', UserModelViewSet, basename='user-api')
router.register(r'friendlist', FriendListViewSet, basename='friendlist-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    path('users_list/', views.users_list, name='users_list'),
    path('user/<slug>/', views.profile_view, name='profile_view'),
    
    path('my-profile/', views.my_profile, name='my_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('friendlist/', views.friend_list, name='friend_list'),
    path('friend-request/send/<int:id>', views.send_friend_request, name='send_friend_request'),
    path('friend-request/cancel/<int:id>', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/accept/<int:id>', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:id>', views.reject_friend_request, name='reject_friend_request'),
    path('friend/unfriend/<int:id>', views.unfriend, name='unfriend'),

]