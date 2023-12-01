from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account.models import Account


@admin.register(Account)
class PersonAdmin(ModelAdmin):
    pass
