from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageModelViewSet, UserModelViewSet
from core.serializers import RecipientView
router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

app_name = 'core'

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('<str:name>/', login_required(
        RecipientView.as_view(template_name='core/chat.html')),name='chat'),
]
