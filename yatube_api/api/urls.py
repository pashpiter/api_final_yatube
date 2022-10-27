from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('group', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments/', CommentViewSet)
router.register('follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
