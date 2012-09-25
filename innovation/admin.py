from django.contrib import admin

from . import models

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Role)
admin.site.register(models.Vote)

