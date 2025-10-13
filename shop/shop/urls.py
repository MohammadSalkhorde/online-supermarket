from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls',namespace='main')),
    path('products/', include('apps.products.urls',namespace='products')),
    path('accounts/', include('apps.accounts.urls',namespace='accounts')),
    path('cs/', include('apps.comment_scoring.urls',namespace='cs')),
    path('orders/', include('apps.orders.urls',namespace='orders')),
    
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)