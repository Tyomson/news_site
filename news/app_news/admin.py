from django.contrib import admin
from .models import News, Comment


# todo Практика
# class CommentInline(admin.TabularInline):
#     model = Comment
#
#
# class NewsAdmin(admin.ModelAdmin):
#     inlines = [CommentInline]
#
#
# class CommentAdmin(admin.ModelAdmin):
#     list_filter = ['name_user']
#
#
# admin.site.register(News, NewsAdmin)
# admin.site.register(Comment, CommentAdmin)


class CommentInline(admin.TabularInline):
    model = Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_news', 'date_create', 'activity']
    list_filter = ['activity']
    inlines = [CommentInline]

    actions = ['mark_as_active', 'mark_as_not_active']

    def mark_as_active(self, request, queryset):
        queryset.update(activity=True)

    def mark_as_not_active(self, request, queryset):
        queryset.update(activity=False)

    mark_as_active.short_description = 'Перевести в статус активно'
    mark_as_not_active.short_description = 'Перевести в статус не активно'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'shortened_comment']
    list_filter = ['username']

    actions = ['mark_as_delete']

    def mark_as_delete(self, request, queryset):
        queryset.update(comment_text='Удалено администратором')

    mark_as_delete.short_description = 'Пометить комментарий как "Удалено администратором"'


admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
