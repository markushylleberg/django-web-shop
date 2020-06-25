from django.contrib import admin
from .models import ProductCategory, Product, ProductAttribute, ProductAttributeOption, ProductVariant, ProductVariantSize, ProductVariantSizeOption, UserProductVariantWishlist, UserProductVariantCart, ShippingMethod, Invoice, InvoiceProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantSize)
admin.site.register(ProductVariantSizeOption)
admin.site.register(ProductCategory)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeOption)
admin.site.register(ShippingMethod)
admin.site.register(UserProductVariantWishlist)
admin.site.register(UserProductVariantCart)
admin.site.register(Invoice)
admin.site.register(InvoiceProduct)
