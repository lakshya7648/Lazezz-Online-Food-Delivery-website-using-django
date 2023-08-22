from django.contrib import admin
from alpha.models import user_account, restaurants, foods, orders
# Register your models here.
admin.site.register(user_account)
admin.site.register(restaurants)
admin.site.register(foods)
admin.site.register(orders)