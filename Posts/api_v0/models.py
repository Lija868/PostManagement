from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=200, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    password_hash = models.CharField(max_length=1000)
    email = models.EmailField(db_index=True,  unique=True,max_length=70, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_image = models.ImageField(null=True, blank=True, upload_to="images/")
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Token(models.Model):
    user_id = models.ForeignKey(User, blank=True,null=True, on_delete=models.DO_NOTHING)
    refresh_token = models.TextField( blank=True, null=True)
    access_token = models.TextField( blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)

class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    title = models.TextField( blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class PostTag(models.Model):
    post_tag_id = models.IntegerField(primary_key= True)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.DO_NOTHING,related_name='post_tags')
    tag = models.TextField( blank=True, null=True)
    weight = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class PostImage(models.Model):
    post_image_id = models.IntegerField(primary_key= True)
    post_id = models.ForeignKey(Post, blank=True, null=True, on_delete=models.DO_NOTHING,related_name='post_images')
    image_url = models.ImageField(null=True, blank=True, upload_to="images/")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post_like_id = models.CharField(primary_key=True, max_length=200, editable=False)
    post_id = models.ForeignKey(Post, blank=True,null=True, on_delete=models.DO_NOTHING, related_name='post_likes')
    user_id = models.ForeignKey(User, blank=True,null=True, on_delete=models.DO_NOTHING)
    is_like = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user_id", "post_id"])]
