from django.test import TestCase

from ..models import Bb, Rubric


class BbModelTestCase(TestCase):

	@classmethod
	def setUpTestData(cls):
		"""
		Задаем настройки глобально для
		данного теста
		:return:
		"""
		# по умолчанию у всех объявлений рубрика должна быть такой
		Rubric.objects.create(name="Без рубрики")
		Bb.objects.create(title="Тестовый заголовок", content='Тестовое описание',
						  price=float(123), rubric=Rubric.objects.get(pk=1))

	def test_max_length_title(self):
		"""
		Тестируем максимальную длину поля title
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		max_length_title = bb._meta.get_field('title').max_length
		self.assertEqual(255, max_length_title)

	def test_title_label(self):
		"""
		Проверка правильности
		описания заголовка поля title
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_title = bb._meta.get_field('title').verbose_name
		self.assertEqual('Товар', label_title)

	def test_help_text_title(self):
		"""
		Тестируем help_text для поля title
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		help_text_title = bb._meta.get_field('title').help_text
		self.assertEqual('Введите название товара (макс. симв. 255)', help_text_title)

	def test_content_null(self):
		"""
		Тестируем установки поля content
		на параметр null
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		null = bb._meta.get_field('content').null
		self.assertTrue(null)

	def test_content_blank(self):
		"""
		Тестируем установки поля content
		на параметр blank
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		blank = bb._meta.get_field('content').blank
		self.assertTrue(blank)

	def test_content_label(self):
		"""
		Тестируем правильность описания
		заголовка поля content
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_content = bb._meta.get_field('content').verbose_name
		self.assertEqual("Описание", label_content)

	def test_price_null(self):
		"""
		Тестируем установки поля price
		на параметр null
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		null = bb._meta.get_field('price').null
		self.assertTrue(null)

	def test_price_blank(self):
		"""
		Тестируем установки поля price
		на параметр blank
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		blank = bb._meta.get_field('price').blank
		self.assertTrue(blank)

	def test_price_label(self):
		"""
		Тестируем правильность описания
		заголовка поля price
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_price = bb._meta.get_field('price').verbose_name
		self.assertEqual("Цена", label_price)

	def test_published_auto_now_add(self):
		"""
		Тестируем установки поля published
		на параметр auto_now_add
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		auto_now_add = bb._meta.get_field('published').auto_now_add
		self.assertTrue(auto_now_add)

	def test_published_db_index(self):
		"""
		Тестируем установки поля published
		на параметр db_index
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		db_index = bb._meta.get_field('published').db_index
		self.assertTrue(db_index)

	def test_published_label(self):
		"""
		Тестируем правильность описания
		заголовка поля published_label
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_published = bb._meta.get_field('published').verbose_name
		self.assertEqual("Опубликовано", label_published)

	def test_last_changed_auto_now(self):
		"""
		Тестируем установки поля last_changed
		на параметр auto_now
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		auto_now = bb._meta.get_field('last_changed').auto_now
		self.assertTrue(auto_now)

	def test_last_changed_label(self):
		"""
		Тестируем правильность описания
		заголовка поля last_changed
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_last_changed = bb._meta.get_field('last_changed').verbose_name
		self.assertEqual("Дата/время последнего изменения записи", label_last_changed)

	def test_rubric_null(self):
		"""
		Тестируем установки поля rubric
		на параметр null
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		null = bb._meta.get_field('rubric').null
		self.assertTrue(null)

	def test_rubric_default_value(self):
		"""
		Тестируем значение по умолчанию
		в поле rubric модели Bb
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		default_rubric = bb._meta.get_field('rubric').default
		self.assertEqual(1, default_rubric)

	def test_rubric_label(self):
		"""
		Тестируем правильность описания
		заголовка поля rubric в модели Bb
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		label_rubric = bb._meta.get_field('rubric').verbose_name
		self.assertEqual("Рубрика", label_rubric)

	def test_rubric_help_text(self):
		"""
		Тестируем правильность написания help_text
		для поля rubric модели Bb
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		help_text_rubric = bb._meta.get_field('rubric').help_text
		self.assertEqual("Выберите рубрику из выпадающего списка", help_text_rubric)

	def test_meta_bb_vnp(self):
		"""
		Тестируем, как будет отображаться имя
		модели во множественном числе
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		verbose_name_plural = bb._meta.verbose_name_plural
		self.assertEqual("объявления", verbose_name_plural)

	def test_meta_bb_vn(self):
		"""
		Тестируем, как будет отображаться имя
		модели в единственном числе
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		verbose_name = bb._meta.verbose_name
		self.assertEqual("объявление", verbose_name)

	def test_meta_bb_ordering(self):
		"""
		Тестируем, по какому полю будет сортировка
		:return:
		"""
		bb = Bb.objects.get(pk=1)
		ordering = bb._meta.ordering
		self.assertEqual("-published", ordering[0])

	def test_first_rubric_max_length(self):
		"""
		Тестируем максимальную длину поля name
		модели Rubric
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		max_length_rubric = rubric._meta.get_field('name').max_length
		self.assertEqual(20, max_length_rubric)

	def test_first_rubric_db_index(self):
		"""
		Тестируем установки поля rubric
		модели Rubric на параметр db_index
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		db_index = rubric._meta.get_field('name').db_index
		self.assertTrue(db_index)

	def test_first_rubric_label(self):
		"""
		Тестируем правильность описания
		заголовка поля name в модели Rubric
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		label_rubric = rubric._meta.get_field('name').verbose_name
		self.assertEqual("Название", label_rubric)

	def test_first_rubric_meta_vnp(self):
		"""
		Тестируем, как будет выглядеть
		название модели во множественном числе
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		verbose_name_plural = rubric._meta.verbose_name_plural
		self.assertEqual("рубрики", verbose_name_plural)

	def test_first_rubric_meta_vn(self):
		"""
		Тестируем, как будет выглядеть
		название модели в единственном числе
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		verbose_name = rubric._meta.verbose_name
		self.assertEqual("рубрика", verbose_name)

	def test_first_rubric_meta_ordering(self):
		"""
		Тестируем, по какому полю будет сортировка
		в модели Rubric
		:return:
		"""
		rubric = Rubric.objects.get(pk=1)
		ordering = rubric._meta.ordering
		self.assertEqual("id", ordering[0])
