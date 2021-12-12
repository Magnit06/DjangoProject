from django.urls import path, reverse_lazy
from django.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, by_rubric, BbCreateView, bb_detail
from .views import SearchResult, users_view
from .views import ads_some_user_view, user_data_detail_view
from .views import edit_user_data

urlpatterns = [
	path('users/profile/change/<str:request_uuid>/', edit_user_data, name="edit_user_data"),
	path('users/profile/ads/<str:uuid>/', ads_some_user_view, name="user_ads"),
	path('users/profile/persons/<str:request_uuid>/', user_data_detail_view, name="person_data"),
	path('detail/<slug:slug>/', bb_detail, name='detail'),
	path('rubric/<str:uuid>/', by_rubric, name='by_rubric'),
	path('users/list/', users_view, name='users_list'),
	path('accounts/login/', LoginView.as_view(), name='login'),
	path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
	path('captcha/', include('captcha.urls')),
	path('add/', BbCreateView.as_view(), name='add'),
	path('search/', SearchResult.as_view(), name='search_result'),
	path('', index, name='index'),
]
