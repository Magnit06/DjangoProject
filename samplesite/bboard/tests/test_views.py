from django.test import TestCase, Client
from django.urls import reverse

from ..models import Rubric, Bb


class ViewsTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		client = Client()
		Rubric.objects.create(name="Без рубрики")
		Bb.objects.create(title="Пример названия товара", content="пример описания товара", price=float(123),
						  rubric=Rubric.objects.get(pk=1))

	def test_response_index(self):
		"""
		Проверка работоспособности
		начальной страницы
		:return:
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(200, response.status_code)

	def test_response_by_rubric(self):
		"""
		Проверка работоспособности
		страницы с выбранной рубрикой
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		response = self.client.get(reverse('by_rubric', args=[bb.rubric.pk]))
		self.assertEqual(200, response.status_code)

	def test_response_add(self):
		"""
		Проверка работоспособности
		страницы с добавлением объявлений
		:return:
		"""
		response = self.client.get(reverse('add'))
		self.assertEqual(200, response.status_code)

	def test_response_search_result(self):
		"""
		Проверка работоспособности страницы
		с результатом поиска
		:return:
		"""
		print(reverse('search_result') + "?q=Пример")
		response = self.client.get(reverse('search_result') + "?q=Прмер")
		self.assertEqual(200, response.status_code)
