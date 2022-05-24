from rest_framework import serializers
from web.models import User, Article, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "bio", "profile_pic")


class ArticleTagListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name


class ArticleSerializer(serializers.ModelSerializer):
    tags = ArticleTagListingField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "tags",
            "title",
            "slug",
            "subtitle",
            "body",
            "author",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "article", "body", "commenter", "created_at", "updated_at")
