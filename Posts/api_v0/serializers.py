from django.db.models import TextField
from rest_framework import serializers

from api_v0.models import *


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=70)
    phone_number = serializers.CharField(max_length=20)
    image = serializers.SerializerMethodField('_image')

    def _image(self, obj):
        print("-----------------------------")
        try:
            image = str(obj.get("user_image"))
            print(image)
        except:
            image = None

        return image

    class Meta:
        model = User
        fields = ("user_id", "first_name", "last_name", "full_name", "email", "phone_number", "image")



class PostImageSerializer(serializers.ModelSerializer):
    post_image_id = serializers.IntegerField()
    image_url = serializers.SerializerMethodField('_image')

    def _image(self, obj):
        try:
            image = str(obj.image_url)
        except:
            image = None

        return image

    class Meta:
        model = PostImage
        fields = ("post_image_id", "image_url")
        depth = 1


class PostTagSerializer(serializers.ModelSerializer):
    post_tag_id = serializers.IntegerField()
    # user_id = serializers.ForeignKey(User, blank=True, null=True, on_delete=serializers.DO_NOTHING)
    tag = TextField()
    weight = serializers.IntegerField()

    class Meta:
        model = PostTag
        fields = ("post_tag_id", "tag", "weight")
        depth = 1

class PostLikeSerializer(serializers.ModelSerializer):
    post_like_id = serializers.CharField()
    # post_id = serializers.ForeignKey(Post, blank=True,null=True, on_delete=serializers.DO_NOTHING)
    # user_id = serializers.ForeignKey(User, blank=True,null=True, on_delete=serializers.DO_NOTHING)
    is_like = serializers.BooleanField(default=False)

    class Meta:
        model = PostLike
        fields = ("post_like_id", "is_like")
        depth = 1



class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()
    title = TextField()
    description = TextField()
    like_count = serializers.IntegerField()
    dislike_count = serializers.IntegerField()
    post_tags = PostTagSerializer(many=True)
    post_images = PostImageSerializer(many=True)
    post_likes = PostLikeSerializer(many=True)

    class Meta:
        model = Post
        fields = ("post_id", "title", "description", "like_count", "dislike_count", "post_tags","post_images", "post_likes")





# class PostLikeSerializer(serializers.ModelSerializer):
#     post_like_id = serializers.CharField()
#     # is_like = serializers.BooleanField(default=False)
#     # post_tags = PostTagSerializer(many=True)
#     posts = PostImageSerializer(many=True)
#
#     class Meta:
#         model = PostLike
#         fields = ("posts")