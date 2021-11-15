from django.urls import path, reverse_lazy
from django.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from .views import index, by_rubric, BbCreateView, BbViewSet, bb_detail
from .views import RubricViewSet, SearchResult, ProfileView, users_view
from .views import some_user_profile_view, CommentViewSet


router = DefaultRouter()
router.register('ads', BbViewSet, basename='ads')
router.register('rubrics', RubricViewSet, basename='rubrics')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
	path('captcha/', include('captcha.urls')),
	path('add/', BbCreateView.as_view(), name='add'),
	path('api/', include(router.urls)),
	path('search/', SearchResult.as_view(), name='search_result'),
	path('detail/<int:rubric_pk>/<int:pk>', bb_detail, name='detail'),
	path('<int:rubric_id>/', by_rubric, name='by_rubric'),
	path('users/profile/<int:pk>/', some_user_profile_view, name="users_profile_detail"),
	path('users/list/', users_view, name='users_list'),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
	path('accounts/profile/', ProfileView.as_view(), name='profile'),
	path('', index, name='index'),
]
