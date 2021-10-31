from django.db import models
from django.contrib.auth.models import User


class Bb(models.Model):
	"""
	Модель объявлений
	"""
	title = models.CharField(max_length=255, verbose_name="Товар",
							 help_text="Введите название товара (макс. симв. 255)")
	content = models.TextField(null=True, blank=True, verbose_name="Описание")
	price = models.FloatField(null=True, blank=True, verbose_name="Цена")
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
	last_changed = models.DateTimeField(auto_now=True, verbose_name="Дата/время последнего изменения записи")
	author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
							   verbose_name="Автор объявления", related_name="author_bboards")
	rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, default="Без рубрики",
							   verbose_name="Рубрика", help_text="Выберите рубрику из выпадающего списка",
							   related_name='bboards')

	def __str__(self):
		return self.title

	class Meta:

		verbose_name_plural = 'объявления'
		verbose_name = 'объявление'
		ordering = ['-published']


class Rubric(models.Model):
	"""
	Модель рубрик
	"""
	name = models.CharField(max_length=20, db_index=True, verbose_name="Название")

	def __str__(self):
		return self.name

	class Meta:

		verbose_name_plural = "рубрики"
		verbose_name = "рубрика"
		ordering = ["id"]


class Comment(models.Model):
	"""
	Модель комментариев
	"""
	author = models.CharField(max_length=100, verbose_name="Автор", db_index=True)
	content = models.TextField(verbose_name='Комментарий')
	bb = models.ForeignKey(Bb, on_delete=models.PROTECT, verbose_name="Объявление")
	created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Время создания")

	def __str__(self):
		return self.author

	class Meta:

		verbose_name_plural = 'комментарии'
		verbose_name = 'комментарий'
		ordering = ['-created_at']

