"""
Данный модуль содержит настройки админ панели
"""
from django.contrib import admin
from django.utils.timezone import make_aware
from django.db.models import Count

# my imports
import datetime as dt
from .models import Bb, Rubric, Comment, ViewsAds
from .models import CustomUser, LogGetParamsAds


class CountCommentsAdFilter(admin.SimpleListFilter):
    """
    Фильтр по комментариям:
    Объявления с самым большим количеством
    комментариев за последний месяц, день, час
    """
    title = "Самое большое количество комментариев у объявления"
    parameter_name = 'created_at'

    def lookups(self, request, model_admin):
        """
        Параметры фильтра
        :param request:
        :param model_admin:
        :return:
        """
        return (
            ('hour', 'За последний час'),
            ('day', 'За последний день'),
            ('month', 'За последний месяц')
        )

    def queryset(self, request, queryset):
        """
        Выполняем фильтрацию для заданных параметров
        :param request:
        :param queryset:
        :return:
        """
        if self.value() == 'hour':
            now_time = make_aware(dt.datetime.now())
            now_time_minus_hour = now_time - dt.timedelta(hours=1)
            return queryset.annotate(count_comment=Count('comment__id')).filter(
                comment__created_at__gte=now_time_minus_hour, comment__created_at__lte=now_time).order_by('-count_comment')

        if self.value() == "day":
            now_time = make_aware(dt.datetime.now())
            now_time_minus_hour = now_time - dt.timedelta(days=1)
            return queryset.annotate(count_comment=Count('comment__id')).filter(
                comment__created_at__gte=now_time_minus_hour, comment__created_at__lte=now_time).order_by('-count_comment')

        if self.value() == "month":
            now_time = make_aware(dt.datetime.now())
            now_time_minus_hour = now_time - dt.timedelta(days=30)
            return queryset.annotate(count_comment=Count('comment__id')).filter(
                comment__created_at__gte=now_time_minus_hour, comment__created_at__lte=now_time).order_by('-count_comment')


class BbAdmin(admin.ModelAdmin):
    """
    Правила отображения объявлений в админ-панели сайта
    """

    list_display = ('title', 'content', 'comment_count', 'published', 'rubric', 'author')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content', 'author__username')
    # указываем django автоматом формировать на основе title slug к url адресу
    prepopulated_fields = {"slug": ("title", )}
    # фильтр по комментариям
    list_filter = (CountCommentsAdFilter,)

    def comment_count(self, obj):
        """
        Количество комментариев у объявления
        :param obj:
        :return:
        """
        return obj.comment_set.count()

    # словесное описание кол-ва комментов в объявлении
    comment_count.short_description = 'Кол-во комментариев'


class CustomUserAdmin(admin.ModelAdmin):
    """
    Правила отображения пользователей в админ-панели
    """
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email', 'last_name')


class RubricAdmin(admin.ModelAdmin):
    """
    Правила отображения рубрик в админ-панели
    """
    list_display = ('id', 'name', 'uuid')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'uuid')


class CommentAdmin(admin.ModelAdmin):
    """
    Правила отображения комментариев в админ-панели
    """
    list_display = ('id', 'author', 'bb_title', 'content', 'created_at')
    list_display_links = ('id', 'author')
    search_fields = ('author', 'content')

    def bb_title(self, obj):
        """
        Отображаем title объявления в комментарии
        :param obj:
        :return:
        """
        return obj.bb.title

    # устанавливаем словесное описание связанной модели
    bb_title.short_description = 'Заголовок объявления'


class LogGetParamsAdsAdmin(admin.ModelAdmin):
    """
    Правила отображения логов
    гет-параметров объявлений в админ-панели
    """
    actions = None
    list_display = ('id_ad', 'slug', 'title', 'author', 'time_visit')
    list_display_links = ('id_ad', 'slug')
    search_fields = ('slug', 'title', 'author')


class ViewsAdsAdmin(admin.ModelAdmin):
    """
    Правила отображения просмотров
    объявлений в админ-панели
    """
    list_display = ('ip', 'views', 'time_views')
    list_display_links = ('ip', 'views')
    search_fields = ('ip', 'views')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LogGetParamsAds, LogGetParamsAdsAdmin)
admin.site.register(ViewsAds, ViewsAdsAdmin)
