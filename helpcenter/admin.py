from django.contrib import admin

from helpcenter import models


class ArticleAdmin(admin.ModelAdmin):
    """ Admin for the Article model """
    date_hierarchy = 'time_published'
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'body')
        }),
        ('Publishing Options', {
            'classes': ('collapse',),
            'fields': ('draft', 'time_published')
        }))
    list_display = (
        'title', 'category', 'time_published', 'time_edited', 'draft')
    search_fields = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    """ Admin for the Category model """
    fieldsets = (
        (None, {
            'fields': ('parent', 'title')
        }),)
    list_display = ('title', 'parent')
    search_fields = ('title',)


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)
