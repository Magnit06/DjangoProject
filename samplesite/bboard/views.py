from django.shortcuts import render

# my import
from django.views.generic.edit import CreateView
from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from .models import Bb
from .models import Rubric
from .forms import BbForm
from .serializers import BbSerializer
from .serializers import RubricSerializer


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