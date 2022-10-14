from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок статьи')
    content = models.TextField(max_length=10000,
                               verbose_name='Контент статьи')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Обложка', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Categories', on_delete=models.PROTECT,
                                 verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comments = GenericRelation('Comments', related_query_name='news')


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Возвращает URL-адрес
        # Функция reverse и тег url в шаблонах - одно и то же, но reverse предпочтительнее
        return reverse('show_news', kwargs={'pk': self.pk})


class Categories(models.Model):
    name = models.CharField(max_length=100,
                            help_text='Выберите категорию',
                            verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def get_absolute_url(self):
        # Возвращает URL-адрес
        # Функция reverse и тег url в шаблонах - одно и то же, но reverse предпочтительнее
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.name


class Comments(models.Model):
    user_comm = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователи')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(max_length=1000, null=True)
    comment_created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-comment_created_at']