from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user_model


class AccountAdmin(UserAdmin):
	list_display = ('email','username', 'is_admin','is_staff')
	search_fields = ('email','username',)
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(user_model, AccountAdmin)