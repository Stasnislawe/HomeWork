from django.contrib.auth.models import AbstractUser
from django.db import models
#from .middleware import get_current_user
from django.db.models import Q
from django.urls import reverse
from .middleware import get_current_user

TN = 'TANK'
HL = 'HILL'
DD = 'DD'
TR = 'TRGV'
GM = 'GLDMSTR'
KG = 'KVSTGIV'
KZ = 'KYZN'
KJ = 'KOZH'
ZV = 'ZLVAR'
MZ = 'MSTRZAK'

cat_list = [(TN, 'Танки'), (HL, 'Хилы'), (DD, 'ДД'), (TR, 'Торговцы'), (GM, 'Гилдмастеры'), (KG, 'Квестгиверы'),
            (KZ, 'Кузнецы'), (KJ, 'Кожевники'), (ZV, 'Зельевары'), (MZ, 'Мастера заклинаний')]


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)

class Advert(models.Model):
    heading = models.CharField(max_length=100, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    time_create = models.DateTimeField(auto_now=True)
    n_files = models.FileField(upload_to='files/%Y/%m/%d', default=None, blank=True,
                               null=True, verbose_name='Файлы')  # Файлы объявления с сортировкой по дате/месяцу/году
    n_photos = models.ImageField(upload_to='photos/%Y/%m/%d', default=None, blank=True,
                                 null=True, verbose_name='Фото')  # Фото объявления с сортировкой по дате/месяцу/году
    cat_name = models.CharField(max_length=7, choices=cat_list, verbose_name='Категория')  # Выбор категории из листа категорий


    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец статьи')

    def __str__(self):
        return '%s: %s-%s' % (self.time_create, self.heading, self.author)

    def get_absolute_url(self):
        return reverse('noti_detail', args=[str(self.id)]) ###

class StatusFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, author_comment = get_current_user()) | Q(status=False, advert_comment__author = get_current_user()) | Q(status=True))

class Comment(models.Model):
    comm_text = models.TextField(verbose_name='Текст коммента')
    comm_time_create = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name='Видимость коммента')

    advert_comment = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='advert_comment')
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    objects = StatusFilterComments()