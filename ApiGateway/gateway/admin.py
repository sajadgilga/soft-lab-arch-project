from django.contrib import admin

# Register your models here.
from gateway.models import API


@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']
