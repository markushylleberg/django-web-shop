from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.urls import reverse

from .models import Product, ProductVariant, ProductAttribute, ProductAttributeOption, ProductCategory, UserProductVariantWishlist


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



def categories(req):
    
    categories_list = Product.objects.values_list('category', flat=True).distinct()
    categories = ProductCategory.objects.filter(id__in=categories_list)

    context = {
        'categories': categories
    }

    if req.method == 'POST':
        category_id = req.POST['category_id']

        category_products = Product.objects.filter(category=category_id)
        category_product_variants = ProductVariant.objects.filter(product=category_products[0])
        category_title = ProductCategory.objects.filter(id=category_id)[0]

        print(category_title)
        # print(categories_list)

        context = {
            'category_products': category_products,
            'category_product_variants': category_product_variants,
            'category_title': category_title
        }

    return render(req, 'pages/products/categories.html', context)



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

    attributes_values_used = ProductAttribute.objects.values('attribute', 'value').distinct()

    attributes_used = ProductAttribute.objects.values_list('attribute', flat=True).distinct()
    attributes = ProductAttributeOption.objects.all().filter(id__in=attributes_used)

    context = {
        'values': attributes_values_used,
        'attributes': attributes
    }

    if req.method == 'POST':
        query_values = []

        for key, value in req.POST.items():
            if key == 'csrfmiddlewaretoken':
                pass
            else:
                query_values.append(f'{value}')


        items_found = []

        for query_value in query_values:
            if query_value:
                items = ProductAttribute.objects.values('entity').filter(Q(value=query_value))
                items_found.append(items)

        filter_count = len(items_found)

        result_list = []

        final_return = []

        for item_found in items_found:
            for item in item_found:
                result_list.append(item['entity'])

        for item in result_list:
            if result_list.count(item) == filter_count:
                final_return.append(item)

        final_return_query_product_variants = ProductVariant.objects.all().filter(id__in=final_return)

        variant_query = ProductVariant.objects.values_list('product', flat=True).filter(id__in=final_return)

        product_query = Product.objects.all().filter(id__in=variant_query)

        context = {
            'values': attributes_values_used,
            'attributes': attributes,
            'products': product_query,
            'product_variants': final_return_query_product_variants
        }
    return render(req, 'pages/products/search.html', context)


@login_required(login_url='/account/login/')
def addtowishlist(req):

    context = {}

    if req.method == 'POST':
        product_variant_id = req.POST['product_variant_id']

        product_variant = ProductVariant.objects.all().filter(id=product_variant_id)[0]

        item_currently_on_wishlist = UserProductVariantWishlist.objects.values_list('product_variant_id', flat=True).filter(Q(user=req.user), Q(product_variant=product_variant_id)).exists()

        if item_currently_on_wishlist:
            pass
        else:
            wishlist_item = UserProductVariantWishlist()
            wishlist_item.user = req.user
            wishlist_item.product_variant = product_variant
            wishlist_item.save()

    return HttpResponseRedirect(reverse('shop:index'))


@login_required(login_url='/account/login/')
def wishlist(req):

    ## Users products and product variants on his/hers wishlist
    wishlist_product_list = list(UserProductVariantWishlist.objects.filter(user=req.user).values_list('product_variant__product_id', flat=True))
    wishlist_product_variants_list = list(UserProductVariantWishlist.objects.filter(user=req.user).values_list('product_variant', flat=True))

    ## Instances of products and product variants
    products = Product.objects.filter(id__in=wishlist_product_list)
    product_variants = ProductVariant.objects.filter(id__in=wishlist_product_variants_list)

    print(products)
    print(product_variants)

    context = {
        'products': products,
        'product_variants': product_variants
    }
    return render(req, 'pages/products/wishlist.html', context)