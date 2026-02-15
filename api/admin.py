from django.contrib import admin
from api.models import Order,OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
class Orderadmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order,Orderadmin)