from django.contrib import admin
from models import Hack


class HacksAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'what', 'where')

admin.site.register(Hack, HacksAdmin)
