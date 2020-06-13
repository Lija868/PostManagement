import os
import uuid

from django.core.files.base import ContentFile
from django.shortcuts import render

# Create your views here.
from django.core.files.storage import default_storage

import hashlib
from datetime import time, datetime
from threading import Thread

import bcrypt
from django.db.models import Q

# Create your views here.
# -*- coding: utf-8 -*-
from api_v0 import serializers
from api_v0.JwtGenerator import jwtGenerator
from api_v0.JwtValidator import jwtValidator
from api_v0.authentication import TokensAuthentication
from api_v0.models import *
from api_v0.pagination import CustomPageNumberPagination
from api_v0.utilities import *
from posts import settings

""" API v0 views."""

from django.views.decorators.cache import cache_control

from rest_framework import response
from rest_framework import schemas
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from rest_framework.response import Response


def schema_view(request):
    """Return v0 API schema."""
    generator = schemas.SchemaGenerator(
        title="True Caller API v0", urlconf="truecaller.api_v0.urls", url="/v0"
    )
    schema = generator.get_schema(request)
    return response.Response(schema)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        response = {}
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_no")
        password = request.data.get("password")
        image = request.data.get("image")

        # display what are the fields which tent to empty.
        validatations = []
        validatations = validateNullOrEmpty(first_name, 702, "First name" , validatations)
        validatations = validateNullOrEmpty(last_name, 703, "Last name" , validatations)
        validatations = validateNullOrEmpty(email, 705, "Email", validatations)
        validatations = validateNullOrEmpty(password, 706, "Password", validatations)

        if len(validatations) > 0:
            resp = {}
            resp["code"] = 600
            resp["validations"] = validatations
            return Response(resp)

        if phone_number:
            if not validate_phone(phone_number):
                return Response({"code": 707, "message": "phone number is not valid"})
        if not validate_email(email):
            return Response({"code": 708, "message": "Email is not valid"})
        if not validate_password(password):
            return Response({"code": 709, "message": "Email is not valid"})



        full_name = first_name + " "+ last_name

        user_obj = User.objects.filter(email=email).count()
        if user_obj >= 1:
            return Response({"code": 710, "message": "Email is already registered, try another Email."})
        else:
            try :
                user_id = hashlib.md5(email.encode() + (str(time)).encode()).hexdigest()
                password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                user_obj = User.objects.create(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    full_name=full_name,
                    password_hash = password_hash,
                    email=email,
                    phone_number=phone_number,
                    user_image=image,

                )
                # t = Thread(target=send_verification, args=(phone_number,))
                # t.start()
                response["code"] = 200
                response["message"] = "ok"
                response["user_id"] = user_obj.user_id
                return Response(response)
            except Exception as e:
                print(e)
                return Response({"code": 114, "message": "Unable to process the request"})

class LoginViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = ()
    authentication_classes = ()

    def create(self, request, *args, **kwargs):

        email = request.data.get("email")
        password = request.data.get("password")
        # display what are the fields which tent to empty.
        validatations = []
        validatations = validateNullOrEmpty(email, 705, "Email", validatations)
        validatations = validateNullOrEmpty(password, 706, "Password", validatations)
        if len(validatations) > 0:
            resp = {}
            resp["code"] = 600
            resp["validations"] = validatations
            return Response(resp)

        try :

            user_obj = User.objects.get(email=email, is_deleted = False)
        except:
            return Response({"code":711,"message":"Invalid Credentials"})

        try:
            password_hash = user_obj.password_hash
            print(password_hash)
            matched = bcrypt.checkpw(password.encode(), password_hash.encode())
            print(matched)

            if (not matched):
                return Response({"code": 711, "message": "invalid credentials"})

            access_token = jwtGenerator(user_obj.user_id,  settings.JWT_SECRET, settings.TOKEN_EXPIRY, "access")
            refresh_token = jwtGenerator(user_obj.user_id,  settings.JWT_SECRET, settings.REFRESH_TOKEN_EXPIRY, "refresh")
            Token.objects.filter(user_id=user_obj).update(is_expired = 1)

            Token.objects.update_or_create(
                user_id=user_obj,
                access_token=access_token,
                refresh_token=refresh_token,
                defaults={"updated_on" : datetime.datetime.now()}
            )

            response_obj = {}
            response_obj["message"] = "ok"
            response_obj["code"] = 200
            response_obj["access_token"] = access_token
            response_obj["refresh_token"] = refresh_token

            return Response(response_obj)
        except Exception as e:
            print(e)
            return Response({"code": 114, "message": "Unable to process the request"})

# class to see any users details passing id
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    authentication_classes = [
       TokensAuthentication
    ]
    permission_classes = ()

    def get_queryset(self):
        user_id = self.kwargs.get("pk", None)
        user_data = User.objects.filter(user_id=user_id).values()
        return user_data

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = [
        TokensAuthentication
    ]
    serializer_class = serializers.PostSerializer
    def get_queryset(self):
        pass

    def filter_queryset(self, queryset):
        """Combined filter queries"""
        post_id = self.kwargs.get("pk", None)

        sort_by = self.request.query_params.get("order_by", None)
        order = self.request.query_params.get("order", "asc")
        title = self.request.query_params.get("title", None)
        description = self.request.query_params.get("descrption", None)

        filters = Q()
        filters &= Q(is_deleted=False)

        if post_id:
            filters &= Q(post_id=post_id)
        if title:
            filters &= Q(title__icontains=title)
        if description:
            filters &= Q(description__icontains=description)
        queryset = Post.objects.filter(filters)
        queryset = queryset.filter(filters)
        if sort_by :
            if order == "asc":
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(sort_by).reverse()

        return queryset

    @cache_control(max_age=0)
    def list(self, request, *args, **kwargs):
        """List a queryset.

        Overrides rest_framework.mixins.ListModelMixin.list() to add a
        cache_control header.
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"result":{}})


class PostLikeViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = [
        TokensAuthentication
    ]
    serializer_class = serializers.PostSerializer
    def get_queryset(self):
        pass

    def filter_queryset(self, queryset):
        """Combined filter queries"""
        token_id = self.request.headers.get("Authorization", "")
        payload = {}

        try:
            payload = jwtValidator(token_id)
            Token.objects.get(access_token=token_id, is_expired=0)
        except:
            return Response({"code": 401, "message": "Expired or Invalid Token"})
        user_id = payload["user_id"]
        try:
            user_obj = User.objects.get(user_id=user_id, is_deleted=0)
        except Exception as e:
            return Response({"code": 114, "message": "Unable to process the request"})

        query = '''
        
select * from api_v0_post p
inner join api_v0_posttag t on p.post_id = t.post_id
left join api_v0_postlike l on t.post_id = l.post_id_id and l.user_id_id = %s and is_like = 1
left join api_v0_postlike dl on t.post_id = dl.post_id_id and dl.user_id_id = %s and dl.is_like = 0
where dl.post_id_id is null
order by ifnull(t.weight,0) desc , p.created_on

        '''
        value_list = []
        value_list.append(user_id)
        value_list.append(user_id)
        qs = Post.objects.raw(query, value_list)

        return qs



    @cache_control(max_age=0)
    def list(self, request, *args, **kwargs):
        """List a queryset.

        Overrides rest_framework.mixins.ListModelMixin.list() to add a
        cache_control header.
        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"result":serializer.data})


    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        is_like = request.data.get("is_like", False)
        token_id = request.headers.get("Authorization", "")
        payload = {}
        if not post_id:
            return Response({"code": 722, "message": "Post id cannot be null or empty"})

        try:
            payload = jwtValidator(token_id)
            Token.objects.get(access_token=token_id, is_expired = 0)
        except:
            return Response({"code": 401, "message": "Expired or Invalid Token"})
        try:
            user_id = payload["user_id"]
            post_obj = Post.objects.get(post_id = post_id, is_deleted = 0)
            if not post_obj:
                return Response({"code": 422, "message": "Post Not Exists"})

            user_obj = User.objects.get(user_id = user_id, is_deleted = 0)
            post_like_id = hashlib.md5(uuid.uuid4().hex.encode() + (str(datetime.datetime.now())).encode()).hexdigest()
            try:
                post_like_obj = PostLike.objects.get(post_id = post_obj, user_id = user_obj)
                post_like_obj.is_like = is_like
                post_like_obj.save()

            except Exception as e:
                PostLike.objects.create(
                    post_like_id = post_like_id,
                    post_id = post_obj,
                    user_id=user_obj,
                    is_like = is_like
                   )

            like_count = post_obj.like_count
            dislike_count = post_obj.dislike_count
            if is_like:
                like_count+=1
            else:
                dislike_count-=1
            post_obj.like_count = like_count
            post_obj.dislike_count = dislike_count
            post_obj.save()
            resp = {}
            resp["code"] = 200
            resp["message"] = "OK"
            return Response(resp)
        except Exception as e:
            print(e)
            return Response({"code": 114, "message": "Unable to process the request"})


class UploadImageViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ()

    def create(self, request,  *args, **kwargs):

        image = request.data.get("image")
        name = "images/" + str(image)
        path = default_storage.save(name, ContentFile(image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        return Response({"code": 200, "msg": "image added successfully.","image_path":path})

class LogoutViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = ()

    def create(self, request,  *args, **kwargs):
        token_id = request.headers.get("Authorization", "")
        try:
            jwtValidator(token_id)
            Token.objects.get(access_token=token_id, is_expired=0)
        except:
            return Response({"code": 401, "message": "Expired or Invalid Token"})
        try:
            token_obj = Token.objects.get(access_token=token_id)
            token_obj.is_expired = 1
            token_obj.save()
            return Response({"code": 200, "message": "ok"})
        except:
            return Response({"code": 114, "message": "Unable to process the request"})

