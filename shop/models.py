from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime


class ProductCategory(models.Model):
    category = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.category}'


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.id}'


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])

    def __str__(self):
        return f'{self.product.title} - {self.image} - {self.price}'


class ProductAttributeOption(models.Model):
    attribute = models.CharField(max_length=180)

    def __str__(self):
        return self.attribute


class ProductAttribute(models.Model):
    entity = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE)
    value = models.CharField(max_length=180)

    def __str__(self):
        return f'{self.entity.product.title} - {self.entity.image} - {self.entity.price}'


class UserProductVariantWishlist(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.get_username()} - {self.product_variant.product.title}'


class UserProductVariantCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total(self):
        return self.product_variant.price * self.quantity

    def __str__(self):
        return f'{self.user} - {self.product_variant}'


class ShippingMethod(models.Model):
    shipping_method = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.shipping_method


class Invoice(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    shipping_method = models.ForeignKey(ShippingMethod, null=True, on_delete=models.SET_NULL)
    transaction_datetime = models.DateTimeField(default=datetime.now, blank=True)
    total_price = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_address = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=120)
    shipping_country = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Confirmed')

    def __str__(self):
        return f'Order #{self.id} --- {self.user}'


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE) ## Should be PROTECT, but for development we'll keep it at CASCADE
    quantity = models.PositiveIntegerField()

    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.invoice} - {self.product}'