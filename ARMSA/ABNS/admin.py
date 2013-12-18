from django.contrib import admin
from .models import Client, Street


class ClientAdmin(admin.ModelAdmin):
    pass


class StreetAdmin(admin.ModelAdmin):
    pass


admin.site.register(Client, ClientAdmin)
admin.site.register(Street, StreetAdmin)
