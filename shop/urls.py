from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .api import InvoiceListAll, InvoiceListConfirmed, InvoiceListShipped, InvoiceDetail

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('decrease_quantity/', views.decrease_quantity, name='decrease_quantity'),
    path('categories/', views.categories, name='categories'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('increase_quantity/', views.increase_quantity, name='increase_quantity'),
    path('product/', views.product_detail, name='product_detail'),
    path('orders', views.orders, name='orders'),
    path('order_detail', views.order_detail, name='order_detail'),
    path('order_overview', views.order_overview, name='order_overview'),
    path('sales_overview', views.sales_overview, name='sales_overview'),
    path('search/', views.search, name='search'),
    path('remove_product_from_cart/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('remove_from_wishlist', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),

    ## Invoices API
    path('api/invoices/', InvoiceListAll.as_view()),
    path('api/invoices/confirmed/', InvoiceListConfirmed.as_view()),
    path('api/invoices/shipped/', InvoiceListShipped.as_view()),
    path('api/invoices/<int:pk>/', InvoiceDetail),
    path('api/invoices/rest-auth/', include('rest_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)