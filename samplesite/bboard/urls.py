from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import index
from .views import by_rubric
from .views import BbCreateView
from .views import BbViewSet
from .views import RubricViewSet
from .views import SearchResult


router = DefaultRouter()
router.register('bboard', BbViewSet, basename='bboard')
router.register('rubrics', RubricViewSet, basename='rubrics')

urlpatterns = [
	path('add/', BbCreateView.as_view(), name='add'),
	path('api/', include(router.urls)),
	path('search/', SearchResult.as_view(), name='search_result'),
	path('<int:rubric_id>/', by_rubric, name='by_rubric'),
	path('', index, name='index'),
]
