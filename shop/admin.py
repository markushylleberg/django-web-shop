from django.contrib import admin
from .models import ProductCategory, Product, ProductAttribute, ProductAttributeOption

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeOption)