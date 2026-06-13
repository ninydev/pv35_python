import graphene
from graphene_django import DjangoObjectType
from news.models import News
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")

class NewsType(DjangoObjectType):
    class Meta:
        model = News
        fields = ("id", "title", "content", "created_at", "created_by", "updated_at", "cover_image")

class Query(graphene.ObjectType):
    all_news = graphene.List(NewsType)
    news_by_id = graphene.Field(NewsType, id=graphene.String())

    def resolve_all_news(root, info):
        return News.objects.all()

    def resolve_news_by_id(root, info, id):
        return News.objects.get(pk=id)

schema = graphene.Schema(query=Query)
