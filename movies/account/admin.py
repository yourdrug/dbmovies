from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account.models import Account, OnlineAccount


@admin.register(Account)
class PersonAdmin(ModelAdmin):
    pass


@admin.register(OnlineAccount)
class PersonAdmin(ModelAdmin):
    pass
