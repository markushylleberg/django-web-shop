from django.utils.crypto import get_random_string
from django.shortcuts import render
from .models import Product, ProductVariant, ProductAttribute

def index(req):

    products = Product.objects.all()
    product_variants = ProductVariant.objects.all()
    product_attributes = ProductAttribute.objects.all()

    context = {
        'products': products,
        'product_variants': product_variants,
        'product_attributes': product_attributes
    }
    return render(req, 'pages/products/index.html', context)



def product_detail(req):

    product_id = req.GET['product_id']
    product_variant_id = req.GET['product_variant_id']

    print(product_id)
    print(product_variant_id)

    product = Product.objects.filter(id=product_id)[0]
    product_variant = ProductVariant.objects.filter(id=product_variant_id)[0]
    product_other_variants = ProductVariant.objects.filter(product=product_id)
    product_attributes = ProductAttribute.objects.filter(entity=product_variant_id)

    print(product_other_variants)

    context = {
        'product': product,
        'product_variant': product_variant,
        'product_other_variants': product_other_variants,
        'product_attributes': product_attributes,
        'quantity': range(1, product_variant.stock + 1)
    }
    return render(req, 'pages/products/product.html', context)



def search(req):

    context = {}

    return render(req, 'pages/products/search.html', context)