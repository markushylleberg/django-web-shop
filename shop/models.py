from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


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