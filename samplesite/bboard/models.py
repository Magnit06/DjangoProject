"""
Модуль моделей проекта
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4


class CustomUser(AbstractUser):

    uuid = models.UUIDField(auto_created=True, unique=True, default=uuid4, db_index=True,
                            verbose_name="Уникальный идентификатор пользователя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество",
                                   db_index=True, help_text="Введите отчество",
                                   null=True, blank=True)
    phone = models.CharField(max_length=18, verbose_name="Номер телефона",
                             db_index=True, help_text="Номер телефона",
                             null=True, blank=True)

    class Meta:

        verbose_name_plural = "пользователи"
        verbose_name = "пользователь"
        ordering = ["username"]


class Bb(models.Model):
    """
    Модель объявлений
    """
    slug = models.SlugField(verbose_name="url", db_index=True,
                            unique=True, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Товар",
                             help_text="Введите название товара (макс. симв. 255)",
                             db_index=True,
                             unique=True)
    content = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    views_counter = models.PositiveIntegerField(null=True, blank=True, db_index=True,
                                                default=0, verbose_name="Количество просмотров")
    author = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name="Автор объявления", related_name="author_bboards")
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, default=1,
                               verbose_name="Рубрика", help_text="Выберите рубрику из выпадающего списка",
                               related_name='bboards')

    def __str__(self):
        """
        Словесное описание модели при добавлении объявления
        :return:
        """
        return self.title

    class Meta:
        """
        Правила отображения модели в админ-панели проекта
        """
        verbose_name_plural = 'объявления'
        verbose_name = 'объявление'
        ordering = ['-title']


class Rubric(models.Model):
    """
    Модель рубрик
    """
    uuid = models.UUIDField(auto_created=True, unique=True, default=uuid4, db_index=True,
                            verbose_name="Уникальный идентификатор записи")
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название")

    def __str__(self):
        """
        Словесное описание модели при добавлении рубрики
        :return:
        """
        return self.name

    class Meta:
        """
        Правила отображения модели в админ-панели проекта
        """
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
        """
        Словесное описание модели при добавлении комментария
        :return:
        """
        return self.author

    class Meta:
        """
        Правила отображения модели в админ-панели проекта
        """
        verbose_name_plural = 'комментарии'
        verbose_name = 'комментарий'
        ordering = ['-created_at']


class LogGetParamsAds(models.Model):
    """
    Модель логов для гет параметров объявлений
    """
    id_ad = models.PositiveIntegerField(db_index=True,
                                     verbose_name='id объявления')
    slug = models.SlugField(db_index=True,
                            verbose_name='Слаг объявления')
    title = models.CharField(max_length=255,
                             db_index=True,
                             verbose_name='Заголовок объявления')
    author = models.CharField(max_length=255,
                              db_index=True,
                              verbose_name='Автор объявления')
    time_visit = models.DateTimeField(auto_now_add=True,
                                      db_index=True,
                                      verbose_name='Время посещения объявления')

    def __str__(self):
        """
        Строковое предстваление
        в админ панели
        :return:
        """
        return self.title

    class Meta:
        """
        Правила отображения модели в админ-панели
        проекта
        """
        verbose_name_plural = "логи объявлений"
        verbose_name = "лог"
        # отображать будем по времени последнего посещения
        ordering = ['-time_visit']


class ViewsAds(models.Model):
    """
    Модель подсчета просмотров объявлений
    """
    ip = models.GenericIPAddressField(db_index=True,
                               verbose_name='IP-адрес посетителя',
                               blank=True, null=True)
    views = models.PositiveIntegerField(db_index=True,
                                        verbose_name='Количество просмотров',
                                        default=0)
    time_views = models.DateTimeField(auto_now=True,
                                      db_index=True,
                                      verbose_name='Дата и время просмотра')
    ad = models.ForeignKey(to=Bb, null=True, blank=True, db_index=True,
                           on_delete=models.PROTECT, verbose_name='Объявление',)

    def __str__(self):
        """
        Строковое представление модели
        :return:
        """
        return self.ip

    class Meta:
        """
        Параметры отображения в админ панели
        """
        verbose_name_plural = 'просмотры объявлений'
        verbose_name = 'просмотр объявления'
        ordering = ['-views']
