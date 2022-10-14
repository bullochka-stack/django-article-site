# создание пользовательких тегов
from django import template
from django.db.models import Count, F

from news.models import Categories

register = template.Library()


# simple тег для получения категорий
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Categories.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)

@register.simple_tag(name='site_title')
def get_title():
    return 'Глашатай'