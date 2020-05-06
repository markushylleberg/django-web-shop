from django.utils.crypto import get_random_string
from django.shortcuts import render
from .models import Product, ProductAttribute

def index(req):

    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.filter(attribute=1)

    print(products)
    print(product_attributes)

    context = {
        'products': products,
        'product_attributes': product_attributes
    }

    return render(req, 'pages/products/index.html', context)

def product_detail(req):

    product_id = req.GET['id']

    product = Product.objects.filter(id=product_id)[0]
    product_attributes = ProductAttribute.objects.filter(entity=product_id)

    print(product_attributes)

    context = {
        'product': product,
        'product_attributes': product_attributes,
        'quantity': range(1, product.stock + 1)
    }

    return render(req, 'pages/products/product.html', context)