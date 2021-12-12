# Create your tasks here
from random import choice, randint
from faker import Faker
from transliterate import slugify

from celery import shared_task
from .models import Rubric, CustomUser, Bb, Comment
from .models import LogGetParamsAds, ViewsAds
from django.db.models import F, Sum
from django.utils.timezone import make_aware
import datetime as dt

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
        user = CustomUser.objects.create_user(username=current_user['username'],
                                        email=current_user['mail'],
                                        password=current_user['username'])  # ради простоты пароль соответствует логину
        print(f"{user.pk} пользователь создан.")
        # сразу же создаем объявления для этого пользователя
        create_ads.delay(user_pk=user.pk, count=count)
    return f"Пользователи сгенерированы, всего {CustomUser.objects.count()}."


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
        current_content = '\n'.join(fake.paragraphs(nb=3))  # пусть будет 3 абзаца
        current_title = fake.word()  # просто слово, так как титул с запасом на кол-во символов
        while True:
            try:
                bb = Bb.objects.create(
                    slug=slugify(current_title),  # формируем slug при генерации данных
                    title=current_title,
                    content=current_content,
                    price=float("".join([choice(num) for _ in range(6)])),
                    rubric=Rubric.objects.get(pk=rubric_pk),
                    author=CustomUser.objects.get(pk=user_pk))
                print(f"{bb.pk} объявление создано.")
            except Exception as e:
                print(f"Такой slug {slugify(current_title)} уже существует!")
                current_title = fake.word()
            else:
                break
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
        user_pk = randint(1, CustomUser.objects.count())
        current_comment = '\n'.join(fake.paragraphs(nb=2))  # пусть будет 2 абзаца
        author = CustomUser.objects.get(pk=user_pk)
        comment = Comment.objects.create(author=author,
                                         content=current_comment,
                                         bb=Bb.objects.get(pk=bb_pk))
        print(f"{comment.pk} комментарий создан.")
    return f"Комментарии созданы, всего {Comment.objects.count()}."


@shared_task
def add_to_log_ads(id_ad, slug, title, author):
    """
    Создаем лог перехода на объявления
    :param id_ad:
    :param slug:
    :param title:
    :param author:
    :return:
    """
    log_ad = LogGetParamsAds.objects.create(id_ad=id_ad, slug=slug,
                                   title=title, author=author)
    return f"+1 переход по ссылке id: {log_ad.id_ad} title: {log_ad.title}"


@shared_task
def increment_view_ad(visitor_ip, bb_pk):
    """
    Увлеичиваем количество просмотра объявления
    :param visitor_ip:
    :param veiw_pk:
    :param bb_pk:
    :return:
    """
    bb = Bb.objects.get(pk=bb_pk)
    # настоящее время
    now_time = make_aware(dt.datetime.now())
    now_time_minus_30_min = now_time - dt.timedelta(seconds=30)  # для теста секунд!!!
    find = False
    for v in bb.viewsads_set.values('ip').all():
        if visitor_ip not in v['ip']:
            continue
        else:
            find = True
            break
    if not find:
        # если таких ip адресов не найдено
        # то создаем и фиксируем время
        ViewsAds.objects.create(ip=visitor_ip,
                            views=1,
                            ad=bb)
    if find:
        # если такой ip уже есть,
        # то проверяем возможность увеличения просмотра
        view = bb.viewsads_set.get(ip=visitor_ip)
        if now_time_minus_30_min > view.time_views:
            # если прошло более 30 минут
            # то увеличиваем просмотр с этим ip на 1
            view.views = F('views') + 1
            view.save()
            view.refresh_from_db()
    # выполняем запрос в БД на получение просмотров со всех ip-адресов
    count = bb.viewsads_set.values('ad_id').annotate(count_views=Sum('views')).order_by('ad_id')
    bb.views_counter = count.first()['count_views']
    bb.save()
    bb.refresh_from_db()
    return f"Просмотры обновлены, теперь у {bb.title} их {bb.views_counter}"
