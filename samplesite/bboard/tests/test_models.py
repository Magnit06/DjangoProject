from django.test import TestCase

from ..models import Bb
from ..models import Rubric


class BbModelTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		# по умолчанию у всех объявлений рубрика должна быть такой
		Rubric.objects.create(name="Без рубрики")
		Bb.objects.create(title="Тестовый заголовок", content='Тестовое описание',
						  price=float(123))

	def test_title_label(self):
		"""
		Проверка правильности
		описания заголовка поля title
		:return:
		"""
		bb = Bb.objects.get(id=1)
		label_title = bb._meta.get_field('title').verbose_name
		self.assertEqual(label_title, 'Товар')

	def test_content_label(self):
		"""
		Тестируем правильность описания
		заголовка поля content
		:return:
		"""
		bb = Bb.objects.get(id=1)
		label_content = bb._meta.get_field('content').verbose_name
		# специально допустил ошибку
		self.assertEqual(label_content, "Описание товара")

	def test_price_label(self):
		"""
		Тестируем правильность описания
		заголовка поля price
		:return:
		"""
		bb = Bb.objects.get(id=1)
		label_price = bb._meta.get_field('price').verbose_name
		self.assertEqual(label_price, "Цена")

	def test_published_label(self):
		"""
		Тестируем правильность описания
		заголовка поля published_label
		:return:
		"""
		bb = Bb.objects.get(id=1)
		label_published = bb._meta.get_field('published').verbose_name
		self.assertEqual(label_published, "Опубликовано")
