from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'user', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_filter = ('created_at', 'updated_at', 'category', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ['id', 'title']
    fields = ('title', 'category', 'user', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'user', 'created_at', 'updated_at', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75px">')
        else:
            return '-'

    get_photo.short_description = 'Изображение'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'user_comm', 'content', 'comment_created_at']
    list_filter = ('comment_created_at', 'user_comm',)
    search_fields = ('content', 'user_comm__username',)
    readonly_fields = ('content_object',)

admin.site.register(News, NewsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Categories)

