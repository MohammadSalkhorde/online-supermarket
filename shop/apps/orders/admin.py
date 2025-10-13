from django.contrib import admin
from .models import *

#====================================================
class OrderDetailsInline(admin.TabularInline):
    model=OrderDetails
    extra=3
#----------------------------------
@admin.register(Order)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display=['customer','register_date','order_state','is_finaly',]
    inlines=[OrderDetailsInline,]
#====================================================
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display=['id','title']
#====================================================
@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['id','warehouse_type_title']
#====================================================
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['product','price','qty','warehouse_type','register_date']
#====================================================
@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=['id','title']
#====================================================
    