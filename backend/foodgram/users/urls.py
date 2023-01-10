from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, delete_token_view, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('token/login/', GetTokenView.as_view()),
    path('token/logout/', delete_token_view),
    path('', include(router.urls)),
]
