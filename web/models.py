from django.forms import ValidationError
from django.template.defaultfilters import slugify
from django.db import models
from utils.codec import codec
from utils.randomizer import random_number

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    bio = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = codec.encrypt(self.password)
        super().save(*args, **kwargs)

    def check_password(self, password):
        return codec.compare(password, self.password)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

    def __str__(self):
        return self.username


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    subtitle = models.CharField(max_length=400, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
            if Article.objects.filter(slug=self.slug).first() != self:
                number = random_number()
                self.slug = slugify(f"{self.title}-{number}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    article = models.ManyToManyField(Article, related_name="tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followee"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.followee}"

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)
        if Follow.objects.filter(
            follower=self.follower, followee=self.followee
        ).exists():
            raise ValidationError("You already follow this user")


class Like(models.Model):
    class Meta:
        unique_together = ("user", "article")

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.article}"
