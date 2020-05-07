from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories', views.categories, name='categories'),
    path('product/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('addtowishlist/', views.addtowishlist, name='addtowishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)