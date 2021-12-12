from django.urls import path, include
from rest_framework import routers

from .views import BbViewSet, CommentViewSet, RubricViewSet

router = routers.DefaultRouter()
router.register('ads', BbViewSet, basename='ads')
router.register('rubrics', RubricViewSet, basename='rubrics')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
