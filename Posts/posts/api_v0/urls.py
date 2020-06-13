# -*- coding: utf-8 -*-
""" API v0 URL configuration."""
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework import routers

from . import views

app_name = "api_v0"

router = routers.DefaultRouter(trailing_slash=False)


router.register(r"register", views.RegisterViewSet, basename="register")
router.register(r"login", views.LoginViewSet, basename="login")
router.register(r"user", views.UserViewSet, basename="user")
router.register(r"logout", views.LogoutViewSet, basename="logout")
router.register(r"upload-image", views.UploadImageViewSet, basename="upload-image")
router.register(r"post", views.PostViewSet, basename="post")
router.register(r"post-like", views.PostLikeViewSet, basename="post-like")

urlpatterns = [path("", views.schema_view), re_path(r"^", include(router.urls))]

