from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from apps.accounts.models import Customer
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order,OrderDetails,PaymentType,OrderState
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
import utils
from .models import Payment,Warehouse,WarehouseType
#--------------------------------------------------------------
class ShopCartVeiw(View):
    def get(self,request, *args, **kwargs):
        shop_cart=ShopCart(request)
        context={
            'shop_cart':shop_cart,
        }
        return render(request,'orders/shop_cart.html',context)
#--------------------------------------------------------------
def show_shop_cart(request):
        shop_cart=ShopCart(request)
        total_price=shop_cart.calc_total_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
        
        context={
            'shop_cart':shop_cart,
            'shop_cart_count':shop_cart.count,
            "total_price":total_price,
            "delivery":delivery,
            "tax":int(tax),
            "order_final_price":int(order_final_price), 
        }
        return render(request,'orders/partials/show_shop_cart.html',context)
#--------------------------------------------------------------
def add_to_shop_cart(request):
    product_id=request.GET.get('product_id')
    qty=request.GET.get('qty')
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,qty)
    return HttpResponse(shop_cart.count)
#--------------------------------------------------------------
def delete_from_shop_cart(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')
#--------------------------------------------------------------
def update_shop_cart(request):
    product_id_list=request.GET.getlist('product_id_list[]')
    qty_list=request.GET.getlist('qty_list[]')
    shop_cart=ShopCart(request)
    shop_cart.update(product_id_list,qty_list)    
    return redirect('orders:show_shop_cart')
#--------------------------------------------------------------
def status_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)
#--------------------------------------------------------------
class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request,order_final_price):
        try:
            customer=Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer=Customer.objects.create(user=request.user)
        
        order=Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType,id=1))
        order.order_state=OrderState.objects.get(id=5)
        order.save()
        Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=request.user),
                amount=order_final_price,
                )
        
        shop_cart=ShopCart(request)
        for item in shop_cart:
            product=Product.objects.get(id=item['product'].id)
            if product.get_number_in_warehouse() >= item['qty']:
                OrderDetails.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                qty=item['qty']
                )
            else:
                message1=f'درحال حاضر فقط تعداد {product.get_number_in_warehouse()} کالا {item['product']} در انبار موجود میباشد'
                message2=f'درحال حاضر کالای {item['product']} در انبار موجود نمیباشد'
                if product.get_number_in_warehouse() == 0:
                    messages.error(request,message2,'danger')
                else:
                    messages.error(request,message1,'danger')
                    
                return redirect('orders:shop_cart')
        return redirect('orders:checkout_order',order.id)
#--------------------------------------------------------------
class CheckoutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):
        user=request.user
        customer=get_object_or_404(Customer,user=user)
        shop_cart=ShopCart(request)
        order=get_object_or_404(Order,id=order_id)
        
        total_price=shop_cart.calc_total_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)

        
        data={
            'name':user.name,
            'family':user.family,
            'email':user.email,
            "phone_number":customer.mobile_number,
            "address":customer.address,
            'description':order.description,
            'payment_type':order.payment_type
            
        }
        form=OrderForm(data)
        context={
            'shop_cart':shop_cart,
            'form':form,
            "total_price":total_price,
            "delivery":delivery,
            "tax":int(tax),
            "order_final_price":int(order_final_price), 
            "order":order, 
        }
        
        return render(request,'orders/checkout.html',context)
    
    def post(self,request,order_id):
        form=OrderForm(request.POST)
        order_final_price = request.POST.get('order_final_price')
        order_final_price=int(order_final_price)
        
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order=Order.objects.get(id=order_id)
                order.description=cd['description']
                order.payment_type = PaymentType.objects.get(id=cd['payment_type'])
                order.save()
                
                user=request.user
                user.name=cd['name']
                user.family=cd['family']
                user.email=cd['email']
                user.save()
                
                customer=Customer.objects.get(user=user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                customer.save()
                
                #چون درگاه پرداخت نداریم جزییات فروش را همینجا ثبت میکنیم
                for item in order.order_details1.all():
                    Warehouse.objects.create(
                        warehouse_type=WarehouseType.objects.get(id=2),
                        user_registered=request.user,
                        product=item.product,
                        qty=item.qty,
                        price=item.price
                    )
                    
                description="پرداخت از طریق درگاه زرین پال"
                payment=Payment.objects.get(order=order)
                if payment:
                    payment.is_finally=True
                    payment.amount=order_final_price
                    payment.save()
                else:
                    payment=Payment.objects.create(
                    order=order,
                    customer=Customer.objects.get(user=request.user),
                    amount=order_final_price,
                    )
                
                    payment.is_finally=True
                    payment.save()
                
                order.is_finaly=True
                order.order_state=OrderState.objects.get(id=1)
                order.save()
                 
                messages.success(request,'سفارش با موفقیت ثبت شد')
                return redirect('main:index')
                
            except ObjectDoesNotExist:
                messages.error(request,'فاکتوری با این مشخصات یافت نشد','danger')
                return redirect('orders:checkout_order', order_id)
        return redirect('orders:checkout_order', order_id)
#---------------------------------------------------------------------
