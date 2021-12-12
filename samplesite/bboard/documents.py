"""
Модуль документа для elasticsearch, задает для него настройки
"""
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Bb, Rubric


@registry.register_document
class BbDocument(Document):
    """
    Задаем настройки как видит elasticsearch модель объявлений
    """

    rubric = fields.NestedField(properties={
        'name': fields.TextField(),
        'pk': fields.IntegerField(),
    })

    class Index:
        """
        Указываем настройки индексации для модели объявлений
        """

        name = 'объявления'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        """
        Показываем как видеть модель Django
        """

        model = Bb
        fields = [
            'title',
            'content',
            'price',
            'published',
        ]
        related_models = [Rubric]

    def get_queryset(self):
        """
        Метод возвращает исходный набор записей,
        из которого будут извлекаться записи
        """
        return super().get_queryset().select_related(
            'rubric'
        )

    def get_instances_from_related(self, related_instance):
        """
        Получаем все объявления от данной рубрики
        :param related_instance: связанная модель
        :return: перечень объявлений для полученной рубрики
        """
        if isinstance(related_instance, Rubric):
            return related_instance.bboards.all()


@registry.register_document
class RubricDocument(Document):
    """
    Задаем настройки как видит elasticsearch модель рубрик
    """

    class Index:
        """
        Указываем настройки индексации для модели рубрик
        """

        name = 'рубрики'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        """
        Показываем как видеть модель Django
        """

        model = Rubric
        fields = [
            'name',
        ]
