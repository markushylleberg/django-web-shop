from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('product/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_product_from_cart/', views.remove_product_from_cart, name='remove_product_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('confirmation/', views.confirmation, name='confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)