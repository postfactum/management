from django.contrib import admin

from .models import Range, Appointment, Reservation


admin.site.register(Range)
admin.site.register(Appointment)
admin.site.register(Reservation)
