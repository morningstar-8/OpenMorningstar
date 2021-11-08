from django.contrib import admin
from Morningstar.models import User
# https://django-import-export.readthedocs.io/en/latest/getting_started.html
from import_export import resources
from import_export.formats import base_formats
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportActionModelAdmin
from .models import Config


class ConfigAdmin(ImportExportModelAdmin):
    list_display = ('username', 'excludeList', )

    def username(self, obj):
        return obj.user.username


admin.site.register(Config, ConfigAdmin)
