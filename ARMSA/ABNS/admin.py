from django.contrib import admin
from .models import client, street


class ClientAdmin(admin.ModelAdmin):
    pass


class StreetAdmin(admin.ModelAdmin):
    pass


admin.site.register(client, ClientAdmin)
admin.site.register(street, StreetAdmin)
