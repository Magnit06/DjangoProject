"""
Данный модуль содержит настройки админ панели
"""
from django.contrib import admin

# my imports
from .models import Bb, Rubric, Comment


class BbAdmin(admin.ModelAdmin):
    """
    Правила отображения объявлений в админ-панели сайта
    """

    list_display = ('title', 'content', 'price', 'published', 'rubric', 'author')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content', 'author')


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(Comment)
