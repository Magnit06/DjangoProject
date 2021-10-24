from django.db import models


class Bb(models.Model):

	title = models.CharField(max_length=255, verbose_name="Товар",
							 help_text="Введите название товара (макс. симв. 255)")
	content = models.TextField(null=True, blank=True, verbose_name="Описание")
	price = models.FloatField(null=True, blank=True, verbose_name="Цена")
	published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
	last_changed = models.DateTimeField(auto_now=True, verbose_name="Дата/время последнего изменения записи")
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

	name = models.CharField(max_length=20, db_index=True, verbose_name="Название")

	def __str__(self):
		return self.name

	class Meta:

		verbose_name_plural = "рубрики"
		verbose_name = "рубрика"
		ordering = ["id"]
