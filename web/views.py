from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from web.models import Article, User
from web.serializers import ArticleSerializer, ProfileSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination

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


class ArticlePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def get_queryset(self, *args, **kwargs):
        query_params = self.request.query_params
        author = query_params.get("author")
        tag = query_params.get("tag")
        if author:
            return self.queryset.filter(author__username=author)
        if tag:
            return self.queryset.filter(tags__name=tag)
        return self.queryset


class ArticleRetrieveView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
