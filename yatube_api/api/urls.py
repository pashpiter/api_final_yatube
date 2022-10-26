from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('group', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments/', CommentViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
