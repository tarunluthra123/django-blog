from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from web.models import Article, User, Comment, ArticleTag
from web.serializers import (
    ArticleSerializer,
    ProfileSerializer,
    UserSerializer,
    CommentSerializer,
)
from rest_framework.pagination import PageNumberPagination
from utils.jwt import encode
from web.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

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


class ArticleRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def patch(self, request, *args, **kwargs):
        user = request.user
        article = self.get_object()
        if article.author != user:
            return Response(
                {"message": "You are not authorized to edit this article"}, status=401
            )
        return self.partial_update(request, *args, **kwargs)


class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        return self.queryset.filter(article__slug=slug)

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        article = Article.objects.get(slug=slug)
        commenter = request.user
        body = request.data.get("body")
        data = {
            "article": article.id,
            "commenter": commenter.id,
            "body": body,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token = encode(user.to_dict())
            serializer = UserSerializer(user)
            return Response({"token": token, **serializer.data})
        return Response({"error": "Invalid Credentials"}, status=401)


class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        tags = data.pop("tags")

        article = Article.objects.create(author=user, **data)

        # tag_ids = []
        # for tag in tags:
        #     tag_ids.append(ArticleTag.objects.get_or_create(name=tag)[0])
        tag_ids = map(lambda tag: ArticleTag.objects.get_or_create(name=tag)[0], tags)

        article.tags.set(tag_ids)

        serializer = ArticleSerializer(article)

        return Response(serializer.data, status=201)
