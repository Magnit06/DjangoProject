# Create your tasks here
from random import choice, randint
from faker import Faker

from celery import shared_task
from .models import Rubric, User, Bb, Comment

fake = Faker(locale=['ru_RU'])


@shared_task
def create_users(count):
    """
    Создаем пользователей
    :param count: кол-во пользователей
    :return:
    """
    for i in range(count):
        current_user = fake.profile()
        user = User.objects.create_user(username=current_user['username'],
                                        email=current_user['mail'],
                                        password=current_user['username'])  # ради простоты пароль соответствует логину
        print(f"{user.pk} пользователь создан.")
        # сразу же создаем объявления для этого пользователя
        create_ads.delay(user_pk=user.pk, count=count)
    return f"Пользователи сгенерированы, всего {User.objects.count()}."


@shared_task
def create_rubrics(count):
    """
    Создаем рубрики
    :param count: кол-во рубрик
    :return:
    """
    for i in range(count):
        # решил использовать текст, так как стоит ограничение в модели
        current_rubric = fake.text(max_nb_chars=20)[:-1]
        rubric = Rubric.objects.create(name=current_rubric)
        print(f"{rubric.pk} рубрика создана.")
    return f"Рубрики созданы, всего {Rubric.objects.count()}."


@shared_task
def create_ads(user_pk, count):
    """
    Создаем объявления
    :param user_pk: id пользователя
    :param count: кол-во объявлений
    :return:
    """
    num = "1234567890"
    for i in range(count):
        rubric_pk = randint(1, Rubric.objects.count())
        current_title = fake.word()  # просто слово, так как титул с запасом на кол-во символов
        current_content = '\n'.join(fake.paragraphs(nb=3))  # пусть будет 3 абзаца
        bb = Bb.objects.create(title=current_title,
                               content=current_content,
                               price=float("".join([choice(num) for _ in range(6)])),
                               rubric=Rubric.objects.get(pk=rubric_pk),
                               author=User.objects.get(pk=user_pk))
        print(f"{bb.pk} объявление создано.")
        # сразу же создаем комментарии к этому объявлению
        create_comments.delay(bb_pk=bb.pk, count=count)
    return f"Объявления созданы, всего {Bb.objects.count()}."


@shared_task
def create_comments(bb_pk, count):
    """
    Создаем комментарии
    :param count: кол-во комментариев
    :param bb_pk: id объявления
    :return:
    """
    for i in range(count):
        user_pk = randint(1, User.objects.count())
        current_comment = '\n'.join(fake.paragraphs(nb=2))  # пусть будет 2 абзаца
        author = User.objects.get(pk=user_pk)
        comment = Comment.objects.create(author=author,
                                         content=current_comment,
                                         bb=Bb.objects.get(pk=bb_pk))
        print(f"{comment.pk} комментарий создан.")
    return f"Комментарии созданы, всего {Comment.objects.count()}."

