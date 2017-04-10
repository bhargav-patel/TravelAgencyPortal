from django.contrib import admin
from portal.models import VehicleCategory, Vehicle, Agency, Booking

# Register your models here.
admin.site.register(VehicleCategory)
admin.site.register(Vehicle)
admin.site.register(Agency)
admin.site.register(Booking)