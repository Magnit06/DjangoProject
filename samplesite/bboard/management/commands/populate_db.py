from random import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bboard.models import Bb, Rubric, Comment


class Command(BaseCommand):
	help = 'Заполняет базу данных тестовыми данными.'

	def handle(self, *args, **options):
		self.stdout.write(self.style.SUCCESS('Процесс наполнения начался...'))
		user_name = "gUser"
		title = "Название товара"
		content = "Описание товара"
		comment = "Комментарий"
		num = "1234567890"
		r = [x for x in range(1, 10)]  # 9
		u = [x for x in range(1, 1001)]  # 1000
		name = "Рубрика"

		print("Генерируем суперпользователя")
		User.objects.create_superuser(username="admin", email="kfilipppov@mail.ru", password="admin")

		print("Генерируем первую рубрику 'Без рубрики'")
		Rubric.objects.create(name="Без рубрики")

		print("Генерируем 9 оставшихся рубрик")
		for i in range(9):
			Rubric.objects.create(name=name + str(i + 1))
		print("Рубрики созданы")

		print("Генерируем 1000 пользователей")
		for i in range(1000):
			User.objects.create_user(username=user_name + str(i + 1),
									 email=user_name + str(i + 1) + "@bboard.ru",
									 password=user_name + str(i + 1))
		print("1000 пользователей создано")

		print("Генерируем для каждого пользователя 1000 объявлений")
		users = User.objects.all()
		for user in users:
			for i in range(1000):
				Bb.objects.create(title=title + " " + str(i + 1) + " " + str(user.username),
								  content=content + " " + str(i + 1) + " " + str(user.username),
								  price=float("".join([random.choice(num) for _ in range(6)])),
								  rubric=Rubric.objects.get(pk=random.choice(r)),
								  author=User.objects.get(pk=user.pk))
		print("1000 объявлений для каждого пользователя созданы")

		print("Генерируем для каждого объявления 1000 комментариев")
		bbs = Bb.objects.all()
		for bb in bbs:
			for i in range(1000):
				author = User.objects.get(pk=random.choice(u))
				Comment.objects.create(author=author,
									   content=comment + " " + str(i + 1) + " " + str(author.username),
									   bb=bb)

		self.stdout.write(self.style.SUCCESS('База данных успешно наполнена!'))
