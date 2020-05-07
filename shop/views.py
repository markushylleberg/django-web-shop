from django.utils.crypto import get_random_string
from django.shortcuts import render
from .models import Product, ProductVariant, ProductAttribute, ProductAttributeOption
from django.db.models import Q

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
                print('ignored csrf token')
            else:
                query_values.append(f'{value}')


        items_found = []

        for query_value in query_values:
            if query_value:
                items = ProductAttribute.objects.values('entity').filter(Q(value=query_value))
                items_found.append(items)
                # for item in items:
                #     items_found.append(item)

        filter_count = len(items_found)

        print(filter_count)
        # print(items_found)

        result_list = []

        final_return = []

        for item_found in items_found:
            # print(item_found)
            for item in item_found:
                # print(item['entity'])
                result_list.append(item['entity'])

        for item in result_list:
            if result_list.count(item) == filter_count:
                final_return.append(item)

        final_return_query = ProductVariant.objects.all().filter(id__in=final_return)

        context = {
            'values': attributes_values_used,
            'attributes': attributes,
            'products': final_return_query
        }

        print(final_return_query)



    return render(req, 'pages/products/search.html', context)