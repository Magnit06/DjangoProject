from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
# my import
from django.views.generic.list import ListView
from elasticsearch_dsl import Q
from transliterate import slugify

from .documents import BbDocument
from .forms import BbForm, CommentForm, CustomUserEditForm
from .models import Bb, Rubric, Comment, CustomUser
from .models import ViewsAds
from .tasks import add_to_log_ads, increment_view_ad


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(bbs, 9)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {"bbs": page.object_list, "rubrics": rubrics, 'page': page}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, uuid):
    bbs = Bb.objects.filter(rubric=Rubric.objects.get(uuid=uuid))
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(uuid=uuid)
    paginator = Paginator(bbs, 9)
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

    def form_valid(self, form):
        """
        здесь мы должны перехватить момент сохранения
        данных в форму и добавить слаг в БД
        :param form:
        :return:
        """
        form.instance.slug = slugify(form.instance.title)
        form.save()
        return super().form_valid(form)


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


@login_required
def bb_detail(request, slug):
    """
    Доступна только для авторизованных пользователей.
    Показывает выбранное объявление, а также позволяет добавить комментарий
    к этому объявлению.
    :param slug:
    :param request:
    :param rubric_pk:
    :param pk:
    :return:
    """
    bb = Bb.objects.get(slug=slug)
    # получаем ip-адрес клиента
    visitor_ip = request.META['REMOTE_ADDR']
    # отдаем задачу на увеличение просмотров объявления
    increment_view_ad.delay(visitor_ip=visitor_ip,
                            bb_pk=bb.pk)
    # отдаем в фоновый процесс создание лога
    add_to_log_ads.delay(id_ad=bb.id,
                         slug=request.GET.get('slug', ''),
                         title=request.GET.get('title', ''),
                         author=request.GET.get('author', ''))
    current_rubric = bb.rubric.name
    rubrics = Rubric.objects.all()
    comments = Comment.objects.filter(bb=bb.pk)
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
    all_users = CustomUser.objects.all()
    rubrics = Rubric.objects.all()
    paginator = Paginator(all_users, 9)
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
def ads_some_user_view(request, uuid):
    """
    Контроллер показывает личную
    страничку выбранного пользователя
    :param request:
    :param pk:
    :return:
    """
    rubrics = Rubric.objects.all()
    some_user = CustomUser.objects.get(uuid=uuid)
    bbs = Bb.objects.filter(author=some_user.pk)
    paginator = Paginator(bbs, 9)
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
    return render(request, 'accounts/some_user_ads.html', context=context)


@login_required
def user_data_detail_view(request, request_uuid):
    """
    показ только авторизированным и подлиным
    пользователям.
    Т к это его ПД
    :param request:
    :param user_uuid:
    :return:
    """
    context = {}
    some_user = CustomUser.objects.get(uuid=request_uuid)
    rubrics = Rubric.objects.all()
    context['some_user'] = some_user
    context['rubrics'] = rubrics
    if request.user.uuid == some_user.uuid:
        # здесь проверяем совпадение uuid авторизированного
        # пользователя и пользователя, которого хотим получить
        # исходя из url параметра
        return render(request=request, template_name='accounts/person_data.html', context=context)
    else:
        # если uuid не совпадают, тогда перенаправляем
        # авторизированного юзера на его страницу
        return redirect(to=reverse(viewname='person_data',
                                   kwargs={'request_uuid': request.user.uuid}))


@login_required
def edit_user_data(request, request_uuid):
    """
    Данная функция будет обрабатывать изменение
    записи личных данных пользователя
    :param request:
    :param request_uuid:
    :return:
    """
    context = {}
    some_user = CustomUser.objects.get(uuid=request_uuid)
    rubrics = Rubric.objects.all()
    context['some_user'] = some_user
    context['rubrics'] = rubrics
    if request.method == 'POST':
        form_edit_user_data = CustomUserEditForm(data=request.POST,
                                                 instance=some_user)
        if form_edit_user_data.is_valid():
            form_edit_user_data.save()
            return redirect(to=reverse(viewname='person_data',
                                       kwargs={'request_uuid': some_user.uuid}))
        else:
            messages.error(request=request,
                           message='Данные, введённые в форму не прошли '
                                   'проверку. Попробуйте ещё раз.')
    # произведем защиту от правки личных данных
    # не правоимеющим пользователем
    if request.user.uuid == some_user.uuid:
        # в таком случае все хорошо
        form_edit_user_data = CustomUserEditForm(instance=some_user)
        context['form'] = form_edit_user_data
        return render(request=request,
                      template_name='accounts/change_data.html',
                      context=context)
    else:
        # перенаправим желающего на правку его данных
        return redirect(to=reverse(viewname='edit_user_data',
                                   kwargs={'request_uuid': request.user.uuid}))