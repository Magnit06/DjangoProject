from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

# my import
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Bb, Rubric, Comment
from .forms import BbForm, CommentForm
from .serializers import BbSerializer, RubricSerializer
from elasticsearch_dsl import Q
from .documents import BbDocument


def index(request):
	bbs = Bb.objects.all()
	rubrics = Rubric.objects.all()
	paginator = Paginator(bbs, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {"bbs": page.object_list, "rubrics": rubrics, 'page': page}
	return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
	bbs = Bb.objects.filter(rubric=rubric_id)
	rubrics = Rubric.objects.all()
	current_rubric = Rubric.objects.get(pk=rubric_id)
	paginator = Paginator(bbs, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {"bbs": page.object_list, "rubrics": rubrics, "current_rubric": current_rubric, 'page': page}
	return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(LoginRequiredMixin, CreateView):

	template_name = 'bboard/create.html'
	form_class = BbForm
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		# добавляем начальное значение автора в форму
		# это поле все равно никто не будет видеть
		self.initial = {'author': self.request.user.pk}
		context = super().get_context_data(**kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context


class BbViewSet(ModelViewSet):

	serializer_class = BbSerializer
	queryset = Bb.objects.all()


class RubricViewSet(ModelViewSet):

	serializer_class = RubricSerializer
	queryset = Rubric.objects.all()


class SearchResult(ListView):

	template_name = 'bboard/search_result.html'
	context_object_name = 'bbs'

	def get_queryset(self):
		"""
		Выдает результат совпадений с запросом поиска
		:return: <class "Bb">
		"""
		query = self.request.GET.get('q')
		q = Q(
				'multi_match',
				query=query,
				fields=[
					'title',
					'content',
				],
				fuzziness='auto')  # корректировка ошибок в запросе
		return BbDocument.search().query(q)

	def get_context_data(self, **kwargs):
		"""
		Создаем и возвращаем контекст шаблона
		:param kwargs:
		:return:
		"""
		context = super().get_context_data(**kwargs)

		# вычисляем длину списка с результатом поиска
		len_search_list = len([x for x in context['bbs']])

		context['len_search_list'] = len_search_list
		context['rubrics'] = Rubric.objects.all()
		return context


class ProfileView(LoginRequiredMixin, ListView):
	"""
	На данную страничку запрещено попадать
	неавторизованным пользователям
	"""
	template_name = 'accounts/profile.html'
	context_object_name = 'bbs'

	def get_queryset(self):
		bbs = Bb.objects.filter(author=User.objects.get(pk=self.request.user.pk))
		paginator = Paginator(bbs, 10)
		if 'page' in self.request.GET:
			page_num = self.request.GET['page']
		else:
			page_num = 1
		self.page = paginator.get_page(page_num)
		return self.page.object_list

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		rubrics = Rubric.objects.all()
		context['rubrics'] = rubrics
		context['page'] = self.page
		return context


@login_required
def bb_detail(request, rubric_pk, pk):
	"""
	Доступна только для авторизованных пользователей
	:param request:
	:param rubric_pk:
	:param pk:
	:return:
	"""
	bb = Bb.objects.get(pk=pk)
	current_rubric = Rubric.objects.get(pk=rubric_pk)
	rubrics = Rubric.objects.all()
	comments = Comment.objects.filter(bb=pk)
	form_class = CommentForm
	initial = {
		'bb': bb.pk,
		'author': request.user.username
	}
	form = CommentForm(initial=initial)
	if request.method == 'POST':
		fill_form = form_class(request.POST)
		if fill_form.is_valid():
			fill_form.save()
			messages.add_message(request, messages.SUCCESS, "Комментарий добавлен.")
		else:
			form = fill_form
			messages.add_message(request, messages.WARNING, "Комментарий не добавлен.")
	context = {
		'rubrics': rubrics,
		'bb': bb,
		'current_rubric': current_rubric,
		'comments': comments,
		'form': form
	}
	return render(request, 'bboard/bb_detail.html', context=context)


@login_required
def users_view(request):
	"""
	Контроллер показывает страницу списка
	пользователей. Для АВТОРИЗИРОВАННЫХ
	:param request:
	:return:
	"""
	all_users = User.objects.all()
	rubrics = Rubric.objects.all()
	paginator = Paginator(all_users, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {
		'all_users': page.object_list,
		'rubrics': rubrics,
		'page': page
	}
	return render(request, 'bboard/users.html', context=context)


@login_required
def some_user_profile_view(request, pk):
	"""
	Контроллер показывает личную
	страничку выбранного пользователя
	:param request:
	:param pk:
	:return:
	"""
	rubrics = Rubric.objects.all()
	some_user = User.objects.get(pk=pk)
	bbs = Bb.objects.filter(author=some_user.pk)
	paginator = Paginator(bbs, 10)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {
		'rubrics': rubrics,
		'some_user': some_user,
		'bbs': page.object_list,
		'page': page
	}
	return render(request, 'accounts/some_user_profile.html', context=context)

