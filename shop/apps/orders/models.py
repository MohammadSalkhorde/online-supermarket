from django.db import models
from apps.accounts.models import Customer,CustomUser
import uuid
import utils
from apps.products.models import Product
from django.utils import timezone
#=========================================================================
class OrderState(models.Model):
    title=models.CharField(max_length=100,verbose_name='وضعیت سفارش')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='وضعیت سفارش'
        verbose_name_plural='انواع وضعیت سفارش'
#=========================================================================
class PaymentType(models.Model):
    title=models.CharField(max_length=100,verbose_name='نوع پرداخت')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name='نوع پرداخت'
        verbose_name_plural='انواع روش پرداخت'
#=========================================================================
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='مشتری',related_name='customer')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت سفارش')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ آپدیت سفارش')
    order_code=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,verbose_name='کد تولیدی برای سفارش')
    order_state=models.ForeignKey(OrderState,default=None,null=True,blank=True,on_delete=models.CASCADE,verbose_name='وضعیت سفارش',related_name='order_states')
    description=models.TextField(verbose_name='توضیحات سفارش')
    payment_type=models.ForeignKey(PaymentType,default=None,on_delete=models.CASCADE,null=True,blank=True,related_name='payment_type',verbose_name='نوع پرداخت')
    is_finaly=models.BooleanField(default=False,verbose_name='نهایی شده')
    
    def __str__(self):
        return f'{self.customer}\t{self.id}\t{self.is_finaly}'
    
    def get_order_total_price(self):
        sum=0
        for item in self.order_details1.all():
            sum+=item.product.price*item.qty
        order_final_price,delivery,tax=utils.price_by_delivery_tax(sum)
        return int(order_final_price*10)
    
    class Meta:
        verbose_name='سفارش'
        verbose_name_plural='سفارشات'
#=========================================================================
class OrderDetails(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سفارش',related_name='order_details1')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='order_details2')
    qty=models.PositiveSmallIntegerField(default=1,verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت کالا در فاکتور')
    
    def __str__(self):
        return f'{self.order}\t{self.product}\t{self.qty}\t{self.price}'
#=========================================================================
class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سفارش',related_name='payment_order')
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name='مشتری',related_name='payment_customer')
    register_date=models.DateTimeField(default=timezone.now,verbose_name='تاریخ پرداخت')
    update_date=models.DateTimeField(auto_now=True,verbose_name='تاریخ ویرایش پرداخت')
    amount=models.IntegerField(verbose_name='مبلغ پرداخت')
    is_finally=models.BooleanField(default=False,verbose_name='وضعیت پرداخت')
    status_code=models.IntegerField(verbose_name='کد وضعیت درگاه پرداخت',null=True,blank=True)
    ref_id=models.CharField(max_length=50,verbose_name='شماره پیگیری پرداخت',null=True,blank=True)
    
    def __str__(self):
        return f'{self.order} {self.customer} {self.ref_id}'
    
    class Meta:
        verbose_name='پرداخت'
        verbose_name_plural='پرداخت ها'
#=========================================================================
class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(max_length=50,verbose_name='نوع انبار')
    
    def __str__(self):
        return self.warehouse_type_title
    
    class Meta:
        verbose_name='نوع انبار'
        verbose_name_plural='انواع روش انبار'
#=========================================================================
class Warehouse(models.Model):
    warehouse_type=models.ForeignKey(WarehouseType,on_delete=models.CASCADE,related_name='Warehouses',verbose_name='انبار')
    user_registered=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='warehouseuser_registered',verbose_name='کاربر')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='warehouse_products',verbose_name='کالا')
    qty=models.IntegerField(verbose_name='تعداد')
    price=models.IntegerField(verbose_name='قیمت واحد',null=True,blank=True)
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    
    def __str__(self):
        return f'{self.warehouse_type} - {self.product}'
    
    class Meta:
        verbose_name='انبار'
        verbose_name_plural='انبار ها'
#=========================================================================
        
