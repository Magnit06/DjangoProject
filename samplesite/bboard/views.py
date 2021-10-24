from django.shortcuts import render

# my import
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from .models import Bb, Rubric
from .forms import BbForm
from .serializers import BbSerializer, RubricSerializer
from elasticsearch_dsl import Q
from .documents import BbDocument
from .documents import RubricDocument


def index(request):
	bbs = Bb.objects.all()
	rubrics = Rubric.objects.all()
	context = {"bbs": bbs, "rubrics": rubrics}
	return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
	bbs = Bb.objects.filter(rubric=rubric_id)
	rubrics = Rubric.objects.all()
	current_rubric = Rubric.objects.get(pk=rubric_id)
	context = {"bbs": bbs, "rubrics": rubrics, "current_rubric": current_rubric}
	return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):

	template_name = 'bboard/create.html'
	form_class = BbForm
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
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
		context = super().get_context_data(**kwargs)

		# вычисляем длину списка с результатом поиска
		len_search_list = len([x for x in context['bbs']])

		context['len_search_list'] = len_search_list
		context['rubrics'] = Rubric.objects.all()
		return context
