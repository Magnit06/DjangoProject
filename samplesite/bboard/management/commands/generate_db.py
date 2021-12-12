from random import choice

from django.core.management.base import BaseCommand

from bboard.models import Bb, Rubric, Comment, CustomUser
from bboard.tasks import create_rubrics, create_users, create_ads, create_comments


class Command(BaseCommand):
	help = 'Заполняет базу данных тестовыми данными.'

	def add_arguments(self, parser):
		parser.add_argument(
			'-n', '--number', default=1000,
			type=int, help='Генерирует "n" образцов пользователей, '
						   'их объявлений, и под каждым объявлением столько же комментариев. '
						   'По умолчанию n=1000.'
		)

	def handle(self, *args, **options):
		self.stdout.write(self.style.SUCCESS('Процесс наполнения начался...'))
		DEFAULT_NUMBER = options['number']
		login_pass_admin = 'admin'

		self.stdout.write(self.style.SUCCESS('Генерируем суперпользователя'))
		CustomUser.objects.create_superuser(username=login_pass_admin, email="kfilipppov@mail.ru", password=login_pass_admin)

		self.stdout.write(self.style.SUCCESS('Генерируем первую рубрику "Без рубрики"'))
		# далее процесс заполнения рубрик уйдет в параллель
		Rubric.objects.create(name="Без рубрики")

		self.stdout.write(self.style.SUCCESS('Генерация 9 оставшихся рубрик запущена'))
		create_rubrics.delay(count=9)

		self.stdout.write(self.style.SUCCESS(f'Генерация {DEFAULT_NUMBER} пользователей запущена'))
		create_users.delay(DEFAULT_NUMBER)

		self.stdout.write(self.style.SUCCESS('Все генерации запущены в фоновые процессы!'))
		self.stdout.write(self.style.SUCCESS('За процессом можете наблюдать а админ панели по адресу:\n'
											 '127.0.0.1:8000/admin/\n'
											 'Данные для входа:\n'
											 f'Login: {CustomUser.objects.get(pk=1).username}\n'
											 f'Password: {CustomUser.objects.get(pk=1).username}'))
