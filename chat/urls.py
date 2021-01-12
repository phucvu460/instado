from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from chat.api import MessageModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/', include(router.urls))
]