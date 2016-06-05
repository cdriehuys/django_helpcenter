from django.contrib import admin

from helpcenter import models


class ArticleAdmin(admin.ModelAdmin):
    """ Admin for the Article model """
    date_hierarchy = 'time_published'
    fieldsets = (
        (None, {
            'fields': ('title', 'body')
        }),
        ('Publishing Options', {
            'classes': ('collapse',),
            'fields': ('time_published',)
        }))
    list_display = ('title', 'time_published')
    search_fields = ('title',)


admin.site.register(models.Article, ArticleAdmin)
