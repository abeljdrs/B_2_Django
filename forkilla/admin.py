from django.contrib import admin
from .models import Restaurant, Reservation, Review

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Reservation)
admin.site.register(Review)