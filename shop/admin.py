from django.contrib import admin
from .models import ProductCategory, Product, ProductAttribute, ProductAttributeOption, ProductVariant, UserProductVariantWishlist

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeOption)
admin.site.register(ProductVariant)
admin.site.register(UserProductVariantWishlist)