from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.registries import registry

from .models import Bb
from .models import Rubric


@registry.register_document
class BbDocument(Document):

	rubric = fields.NestedField(properties={
		'name': fields.TextField(),
		'pk': fields.IntegerField(),
	})

	class Index:

		name = 'объявления'
		settings = {
			'number_of_shards': 1,
			'number_of_replicas': 0
		}

	class Django:

		model = Bb
		fields = [
			'title',
			'content',
			'price',
			'published',
			'last_changed',
		]
		related_models = [Rubric]

	def get_queryset(self):
		"""
		Метод возвращает исходный набор записей,
		из которого будут извлекаться записи
		"""
		return super(BbDocument, self).get_queryset().select_related(
			'rubric'
		)

	def get_instances_from_related(self, related_instance):
		if isinstance(related_instance, Rubric):
			return related_instance.bboards.all()


@registry.register_document
class RubricDocument(Document):

	class Index:

		name = 'рубрики'
		settings = {
			'number_of_shards': 1,
			'number_of_replicas': 0
		}

	class Django:

		model = Rubric
		fields = [
			'name',
		]
