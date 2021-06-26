from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    title_news = models.CharField(max_length=1000, db_index=True, verbose_name='название')
    content = models.CharField(max_length=10000, default='', verbose_name='содержание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
    activity = models.BooleanField(default=False, verbose_name='флаг активности')
    tag = models.CharField(default='', max_length=15, verbose_name='тег новости')

    class Meta:
        ordering = ['date_create']
        verbose_name = 'новость'
        verbose_name_plural = 'новость'

    def __str__(self):
        return f'{self.title_news}, {self.date_create}, {self.date_edit}, {self.activity}'


class Comment(models.Model):
    username = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE,
                                 related_name='comment', verbose_name='имя пользователя')
    comment_text = models.CharField(max_length=1000, default='', verbose_name='комментарий пользователя')
    title_news = models.ForeignKey('News', default=None, null=True, on_delete=models.CASCADE,
                                   related_name='comment', verbose_name='новость')

    def shortened_comment(self):
        if len(self.comment_text) < 15:
            return f'{self.comment_text}'
        return f'{self.comment_text[0:15]}...'

    def __str__(self):
        return f'{self.username}, {self.comment_text}, {self.title_news}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True, verbose_name='город')
    phone_number = models.CharField(max_length=11, blank=True, verbose_name='номер телефона')
    number_published_news = models.IntegerField(default=0, blank=False, verbose_name='количество опубликованных '
                                                                                     'новостей')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        permissions = (
            ('can_write', 'Может писать новость'),
            ('can_publish', 'Может публиковать новость'),
            ('can_verify', 'Может верифицировать пользователей'),
        )
