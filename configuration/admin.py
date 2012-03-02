# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Config


class ConfigAdmin(admin.ModelAdmin):
    save_on_top = True

    def has_add_permission(self, request):
        return False if Config.objects.count() else super(ConfigAdmin, self).has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Config, ConfigAdmin)
