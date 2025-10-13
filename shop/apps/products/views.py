from django.shortcuts import render,redirect
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from .filter import *
#===========================================================================
#ارزانترین محصولات
def get_cheapset_products(request ,*args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:12]
    product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))[:7]
    
    context={
        'products':products,
        'product_groups':product_groups
    }
    
    return render(request,'products/partials/cheapset_products.html',context)
#===========================================================================
#جزئیات محصول
class ProductDetailView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        if product.is_active:
            return render(request,'products/product_detail.html',{'product':product})
#===========================================================================
def get_filter_value_for_feature(request):
    if request.method=='GET':
        feature_id = request.GET['feature_id']
        feature_value = FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_value}
        return JsonResponse(data=res,safe=False)
#===========================================================================
def get_related_products(request ,*args, **kwargs):
    current_product=get_object_or_404(Product,slug=kwargs['slug'])
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    return render(request,'products/partials/related_products.html',{'related_products':related_products})
#===========================================================================
def get_last_products(request):
    products=Product.objects.filter(is_active=True).order_by('-register_date')[:5]
    
    return render(request,'products/partials/last_products.html',{'products':products})
#===========================================================================
def get_all_subgroups(group):
    subgroups = list(group.groups.all())
    for subgroup in group.groups.all():
        subgroups += get_all_subgroups(subgroup)
    return subgroups
#===========================================================================
class ProductGroupsView(View):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(
            Q(is_active=True) & Q(group_parent=None)
        )

        # محاسبه تعداد کل محصولات (خود گروه + زیرگروه‌ها)
        for group in product_groups:
            all_subgroups = get_all_subgroups(group)
            all_groups = [group] + all_subgroups
            product_count = Product.objects.filter(
                product_group__in=all_groups,
                is_active=True
            ).distinct().count()
            group.total_products = product_count

        # مرتب‌سازی بر اساس تعداد محصول از بیشتر به کمتر
        product_groups = sorted(product_groups, key=lambda g: g.total_products, reverse=True)

        return render(request, 'products/product_groups.html', {
            'product_groups': product_groups
        })
#===========================================================================
# تابع بازگشتی برای گرفتن همه زیرگروه‌ها
def get_all_subgroups(group):
    subgroups = []
    for sub in group.groups.filter(is_active=True): 
        subgroups.append(sub)
        subgroups.extend(get_all_subgroups(sub))
    return subgroups
#===========================================================================
def get_popular_product_groups(request):
    # گرفتن گروه‌های اصلی فعال
    product_groups = ProductGroup.objects.filter(
        Q(is_active=True) & Q(group_parent=None)
    )

    # محاسبه تعداد کل محصولات (خود گروه + زیرگروه‌ها)
    for group in product_groups:
        all_subgroups = get_all_subgroups(group)
        all_groups = [group] + all_subgroups
        total_products = Product.objects.filter(
            product_group__in=all_groups,
            is_active=True
        ).distinct().count()
        group.total_products = total_products  # فیلد موقت برای قالب

    # مرتب‌سازی بر اساس تعداد محصول از بیشتر به کمتر
    product_groups = sorted(product_groups, key=lambda g: g.total_products, reverse=True)[:6]

    return render(request, 'products/partials/popular_product_groups.html', {
        'product_groups': product_groups
    })
#===========================================================================
def get_all_subgroups(group):
    subgroups = list(group.groups.all())
    for subgroup in group.groups.all():
        subgroups += get_all_subgroups(subgroup)
    return subgroups
#===========================================================================
class ProductByGroupsView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)

        # تمام زیرگروه‌ها (به صورت بازگشتی)
        all_subgroups = get_all_subgroups(current_group)
        all_groups = [current_group] + all_subgroups  # خود گروه فعلی + زیرگروه‌ها

        # همه‌ی محصولات مرتبط با این گروه‌ها
        products = Product.objects.filter(product_group__in=all_groups, is_active=True).distinct()

        # جمع حداقل و حداکثر قیمت
        res_aggre = products.aggregate(min=Min('price'), max=Max('price'))

        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs

        brands_filter = request.GET.getlist('brand')
        if brands_filter:
            products = products.filter(brand__id__in=brands_filter)

        features_filter = request.GET.getlist('feature')
        if features_filter:
            products = products.filter(product_features__filter_value__id__in=features_filter).distinct()

        if features_filter:
            products=products.filter(product_features__filter_value__id__in=features_filter).distinct()
        
        # مرتب‌سازی
        sort_type = request.GET.get('sort_type', "0")
        if sort_type == "1":
            products = products.order_by('price')
        elif sort_type == "2":
            products = products.order_by('-price')

        # صفحه‌بندی
        group_slug = slug
        product_per_page = 5
        product_count = products.count()

        show_count = request.GET.get('show_count', product_per_page)
        try:
            show_count = int(show_count)
        except ValueError:
            show_count = product_per_page

        paginator = Paginator(products, show_count)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        show_count_product = []
        i = product_per_page
        while i < product_count:
            show_count_product.append(i)
            i *= 2
        show_count_product.append(product_count)

        context = {
            'products': products,
            "current_group": current_group,
            'res_aggre': res_aggre,
            'group_slug': group_slug,
            'page_obj': page_obj,
            'product_count': product_count,
            'filter': filter,
            'sort_type': sort_type,
            'show_count_product': show_count_product,
            'show_count': show_count,
            'product_groups': current_group.groups.filter(is_active=True),
            }

        return render(request, 'products/products_by_group.html', context)

#===========================================================================
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_groups'))\
        .filter(Q(is_active=True) & ~Q(count=0))\
        .order_by('-count')
        
    return render(request,'products/partials/products_groups.html',{'product_groups':product_groups})
#===========================================================================
def get_brands(request, *args, **kwargs):
    product_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id=product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id)\
        .annotate(count=Count('brands'))\
        .filter(~Q(count=0))\
        .order_by('-count')
        
    return render(request,'products/partials/brands.html',{'brands':brands})
#===========================================================================
def get_features_for_filter(request,*args, **kwargs):
    product_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list=product_group.features_of_groups.all()
    feature_dict={}
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all()
        
    return render(request,'products/partials/features_filter.html',{'feature_dict':feature_dict})
#===========================================================================
class SearchResualtsView(View):
    def get(self,request,*args, **kwargs):
        query=self.request.GET.get('q')
        products=Product.objects.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
        
        context={
            'products':products
        }
        
        return render(request,'search/search_resualt.html',context)
#===========================================================================
def get_sell():
    products = Product.objects.all()
    dict1 = {}
    for i in products:
        sell = i.get_sell() or 0  # اگر None بود، صفر قرار بده
        dict1[i.id] = sell
    return dict1
#===========================================================================
def get_best_sellers(request, limit=5):
    sell_data = get_sell() 

    sorted_products = sorted(
        ((pid, sell or 0) for pid, sell in sell_data.items()),
        key=lambda x: x[1],
        reverse=True
    )

    top_ids = [pid for pid, _ in sorted_products[:limit]]

    best_sellers = Product.objects.filter(id__in=top_ids)[:6]

    return render(request, 'products/partials/best_sellers.html', {'products': best_sellers})
#===========================================================================
