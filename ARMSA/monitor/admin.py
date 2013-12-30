from django.contrib import admin
from .models import ControlPoint, Group


class GroupAdmin(admin.ModelAdmin):
    pass


class ControlPointAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(ControlPoint, ControlPointAdmin)
