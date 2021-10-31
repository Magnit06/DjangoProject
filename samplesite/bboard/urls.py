from django.urls import path, reverse_lazy
from django.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from .views import index, by_rubric, BbCreateView, BbViewSet, bb_detail
from .views import RubricViewSet, SearchResult, ProfileView


router = DefaultRouter()
router.register('bboard', BbViewSet, basename='bboard')
router.register('rubrics', RubricViewSet, basename='rubrics')

urlpatterns = [
	path('captcha/', include('captcha.urls')),
	path('add/', BbCreateView.as_view(), name='add'),
	path('api/', include(router.urls)),
	path('search/', SearchResult.as_view(), name='search_result'),
	path('detail/<int:rubric_pk>/<int:pk>', bb_detail, name='detail'),
	path('<int:rubric_id>/', by_rubric, name='by_rubric'),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
	path('accounts/profile/', ProfileView.as_view(), name='profile'),
	path('', index, name='index'),
]
