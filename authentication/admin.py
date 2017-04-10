from django.contrib import admin
from authentication.models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','mobile','address')
	# list_filter = ('mobile',)
	search_fields = ['user__username','user__first_name','user__last_name','mobile','address']

admin.site.register(Profile,ProfileAdmin)
