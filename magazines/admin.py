# Django
from django.contrib import admin

# Local Django
from .models import Publisher, Number, Magazine, Article


class Magazines(admin.ModelAdmin):
    list_display = ('magazine_name', 'publisher_name', 'number', 'pub_date')
    list_filter = ['magazine_name']
    search_fields = ['magazine_name']


class Articles(admin.ModelAdmin):
    list_display = ('headline', 'text', 'subject', 'users_name',
                    'number', 'pub_date')
    list_filter = ['headline']
    search_fields = ['headline']


admin.site.register(Publisher)
admin.site.register(Number)
admin.site.register(Magazine,Magazines)
admin.site.register(Article,Articles)

# Register your models here.
