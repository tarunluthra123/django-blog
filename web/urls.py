from django.urls import path
from web.views import (
    LoginView,
    ProfileRetrieveView,
    UserView,
    PingPongView,
    ProfileListView,
    ArticleListView,
    ArticleRetrieveView,
    CommentListView,
)

urlpatterns = [
    path("ping/", PingPongView.as_view()),
    path("users/", UserView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("profiles/", ProfileListView.as_view()),
    path("profiles/<username>", ProfileRetrieveView.as_view()),
    path("articles/", ArticleListView.as_view()),
    path("articles/<slug>", ArticleRetrieveView.as_view()),
    path("articles/<slug>/comments/", CommentListView.as_view()),
]
