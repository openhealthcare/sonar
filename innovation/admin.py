from django.contrib import admin

from . import models


admin.site.register(models.Item)
admin.site.register(models.Evidence)
admin.site.register(models.Role)
admin.site.register(models.Specialisation)
admin.site.register(models.Vote)

