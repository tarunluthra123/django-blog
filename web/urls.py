from django.urls import path
from web.views import (
    ProfileRetrieveView,
    UserView,
    PingPongView,
    ProfileListView,
    ArticleListView,
)

urlpatterns = [
    path("ping/", PingPongView.as_view()),
    path("users/", UserView.as_view()),
    path("profiles/", ProfileListView.as_view()),
    path("profiles/<username>", ProfileRetrieveView.as_view()),
    path("articles/", ArticleListView.as_view()),
]
