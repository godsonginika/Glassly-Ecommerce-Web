from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'delivery_area', 'total', 'created_at']
    search_fields = ['full_name', 'phone']
    inlines = [OrderItemInline]