from django.db import models
from django.core.validators import FileExtensionValidator


class ProductCategory(models.Model):
    category = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.category}'


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])

    def __str__(self):
        return self.title


class ProductAttributeOption(models.Model):
    attribute = models.CharField(max_length=180)

    def __str__(self):
        return self.attribute


class ProductAttribute(models.Model):
    entity = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE)
    value = models.CharField(max_length=180)

    def __str__(self):
        return f'{self.value}'
