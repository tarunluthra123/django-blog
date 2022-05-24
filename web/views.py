from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from web.models import Article, User
from web.serializers import ArticleSerializer, ProfileSerializer, UserSerializer

# Create your views here.
class PingPongView(APIView):
    def get(self, request):
        return Response({"message": "pong"})


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "username"


class ProfileListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, *args, **kwargs):
        out = self.list(*args, **kwargs)
        return out
