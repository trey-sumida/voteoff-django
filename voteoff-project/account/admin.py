from django.contrib import admin
from .models import Account, AccountDemographics
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AccountDemographicsAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'last_name', 'visibility', 'points')
    search_fields = ('first_name', 'last_name')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountDemographics, AccountDemographicsAdmin)
