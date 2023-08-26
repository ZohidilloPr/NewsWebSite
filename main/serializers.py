from .models import (
    Comments, Ads,
    News, Category, MainNews
)
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes



class CategoryMS(serializers.ModelSerializer):
    """ Newsni categorilari uchun """
    class Meta:
        model = Category
        fields = "__all__"


class NewsMS(serializers.ModelSerializer):
    """ Yangiliklar uchun JSON data chiqarish """
    html = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)

    @extend_schema_field(OpenApiTypes.DATETIME)    
    def get_html(self, instance): # QUILFILD datani JSON qilish
        return str(instance.post.html)

    class Meta:
        model = News
        fields = (
            "id", "pk", "slug", "title", "subtitle", "post", "html",
            "post_img", "post_video", "post_file", 
            "comment_on_off", "favorite", "status", "breaking_news", "post_view", "comment_count",
            "author_news", "add_time", "update_time", "category",  
        )
        # depth = 1


class CommentMS(serializers.ModelSerializer):
    """ Izoh yozish """
    class Meta:
        model = Comments
        fields = ("id", "pk", "f_name", "comment", "add_time", "news")


class MainNewsSerializers(serializers.ModelSerializer):
    """ ASOSIY WEB SAHIFADA KO'RINADIGAN YANGILIKLAR """
    posts = NewsMS(many=True)

    class Meta:
        model = MainNews
        fields = [
            "id", "pk", "category", "posts", 
        ]


class AdsMs(serializers.ModelSerializer):
    """ REKLAMALAR """

    class Meta:
        model = Ads
        fields = [
            "id", "pk", "ads_video", "ads_image", "note",
            "status", "location", "link", "add_time", "update_time"
        ]
        depth = 1


