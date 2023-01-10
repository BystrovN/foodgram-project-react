from django.urls import path

from .views import GetTokenView, delete_token_view


urlpatterns = [
    path('token/login/', GetTokenView.as_view()),
    path('token/logout/', delete_token_view),
]
