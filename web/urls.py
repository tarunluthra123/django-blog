from django.urls import path
from web.views import UserView, PingPongView

urlpatterns = [
    path("ping/", PingPongView.as_view()),
    path("users/", UserView.as_view()),
]
