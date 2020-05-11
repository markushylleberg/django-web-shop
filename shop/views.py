from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.urls import reverse

from .models import Product, ProductVariant, ProductAttribute, ProductAttributeOption, ProductCategory, UserProductVariantWishlist, UserProductVariantCart, ShippingMethod, Invoice, InvoiceProduct
from account.models import UserProfile


def index(req):

    products = Product.objects.all()
    product_variants = ProductVariant.objects.all()
    product_attributes = ProductAttribute.objects.all()

    product_variants_list = ProductVariant.objects.values_list('id', flat=True)
    product_variants_currently_in_carts = UserProductVariantCart.objects.values_list('product_variant', flat=True)


    context = {
        'products': products,
        'product_variants': product_variants,
        'product_attributes': product_attributes,
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

    product = Product.objects.filter(id=product_id)[0]
    product_variant = ProductVariant.objects.filter(id=product_variant_id)[0]
    product_other_variants = ProductVariant.objects.filter(product=product_id)
    product_attributes = ProductAttribute.objects.filter(entity=product_variant_id)

    product_variant_currently_in_carts = list(UserProductVariantCart.objects.filter(product_variant=product_variant.id).values_list('quantity', flat=True))

    total_amount_in_carts = 0

    for product_variant_currently_in_cart in product_variant_currently_in_carts:
        total_amount_in_carts += product_variant_currently_in_cart

    context = {
        'product': product,
        'product_variant': product_variant,
        'product_other_variants': product_other_variants,
        'product_attributes': product_attributes,
        'quantity': range(1, product_variant.stock + 1 - total_amount_in_carts)
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


def cart(req):

    context = {}

    if req.user.is_authenticated:
        cart_products = list(UserProductVariantCart.objects.filter(user=req.user).values_list('product_variant', flat=True))

        cart_product_quantity = UserProductVariantCart.objects.filter(user=req.user)

        product_variants = ProductVariant.objects.filter(id__in=cart_products)


        product_variants_list = ProductVariant.objects.filter(id__in=cart_products).values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=product_variants_list)

        cart_total = 0

        for item in cart_product_quantity:
            cart_total += item.total()

        context = {
            'cart_product_quantities': cart_product_quantity,
            'cart_products': cart_products,
            'product_variants': product_variants,
            'products': products,
            'cart_total': cart_total
        }
    
    return render(req, 'pages/products/cart.html', context)


def add_to_cart(req):
    if req.method == 'POST':
        product_variant_id = req.POST['product_variant_id']
        quantity = req.POST['quantity']

        ## Check if item is in database and in the requested stock amount
        is_product_available = ProductVariant.objects.filter(Q(id=product_variant_id), Q(stock__gte=quantity)).exists()
        if is_product_available:
            if req.user.is_authenticated:
                product_already_in_cart = UserProductVariantCart.objects.filter(Q(user=req.user), Q(product_variant=product_variant_id))
                if product_already_in_cart:
                    product_already_in_cart[0].quantity += int(quantity)
                    product_already_in_cart[0].save()
                else:
                    product = ProductVariant.objects.filter(id=product_variant_id)[0]
                    user = req.user
                    new_cart_product = UserProductVariantCart()
                    new_cart_product.product_variant = product
                    new_cart_product.quantity = quantity
                    new_cart_product.user = user
                    new_cart_product.save()
            else:
                print('User is NOT logged in. We need to store this cart item someplace')
        else:
            print('Something went wrong - product is not available in that quantity!')
    
    return HttpResponseRedirect(reverse('shop:cart'))


def increase_quantity(req):

    if req.method == 'POST':
        product_variant = req.POST['product_variant_id']
        user = req.user
        if user.is_authenticated:
            product_variant_currently_in_carts = list(UserProductVariantCart.objects.filter(product_variant=product_variant).values_list('quantity', flat=True))

            total_amount_in_carts = 0

            for product_variant_currently_in_cart in product_variant_currently_in_carts:
                total_amount_in_carts += product_variant_currently_in_cart

            product_variant_stock = ProductVariant.objects.values_list('stock', flat=True).filter(id=product_variant)[0]

            if product_variant_stock == total_amount_in_carts:
                print('not available at the moment')
            else:
                user_cart_product = UserProductVariantCart.objects.filter(Q(user=user), Q(product_variant=product_variant))[0]
                user_cart_product.quantity += 1
                user_cart_product.save()
        else:
            print('we need to change the quantity in the cookie of an unnauthenticated user')

    return HttpResponseRedirect(reverse('shop:cart'))


def decrease_quantity(req):

    if req.method == 'POST':
        if req.user.is_authenticated:
            product_variant = req.POST['product_variant_id']
            user = req.user

            user_cart_product = UserProductVariantCart.objects.filter(Q(user=user), Q(product_variant=product_variant))[0]

            if user_cart_product.quantity == 1:
                user_cart_product.delete()
            else:
                user_cart_product.quantity -= 1
                user_cart_product.save()
        else:
            print('we need to change the quantity in the cookie of an unnauthenticated user')

    return HttpResponseRedirect(reverse('shop:cart'))


def remove_product_from_cart(req):

    if req.method == 'POST':
        if req.user.is_authenticated:
            product_variant = req.POST['product_variant_id']
            user = req.user

            user_cart_product = UserProductVariantCart.objects.filter(Q(user=user), Q(product_variant=product_variant))[0]
            user_cart_product.delete()
        else:
            print('we need to do remome this item from a cookie in a unauthenticated user')

    return HttpResponseRedirect(reverse('shop:cart'))


@login_required(login_url='/account/login/')
def add_to_wishlist(req):

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


def checkout(req):

    context = {}

    if req.user.is_authenticated:
        user = UserProfile.objects.filter(user=req.user.id)
        cart_products = UserProductVariantCart.objects.select_related('product_variant').filter(user=req.user)
        shipping_methods = ShippingMethod.objects.all()

        cart_total = 0

        for cart_product in cart_products:
            cart_total += cart_product.total()

        context = {
            'cart_total': cart_total,
            'cart_products': cart_products,
            'user_profile': user[0],
            'shipping_methods': shipping_methods
        }
        

    else:
        print('we need to show the cart products from a cookie from a unauthenticated user')

    return render(req, 'pages/products/checkout.html', context)


def confirm_order(req):

    first_name = req.POST['checkout_firstname']
    last_name = req.POST['checkout_lastname']
    address = req.POST['checkout_address']
    city = req.POST['checkout_city']
    country = req.POST['checkout_country']
    phone = req.POST['checkout_phone']

    shipping_method = req.POST['checkout_shipping_method']
    payment_method = req.POST['checkout_payment_method']

    cart_products = UserProductVariantCart.objects.filter(user=req.user)
    shipping = ShippingMethod.objects.filter(id=shipping_method)[0]

    cart_total = 0

    for cart_product in cart_products:
        cart_total += cart_product.total()

    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'country': country,
        'phone': phone
    }

    context = {
        'cart_total': cart_total,
        'shipping': shipping,
        'cart_products': cart_products,
        'user_profile': user_data
    }

    return render(req, 'pages/products/confirm_order.html', context)


def confirmation(req):

    if req.method == 'POST':
        if req.user.is_authenticated:
            user = req.user
            email = req.POST['confirm_email']
            address = req.POST['confirm_address']
            city = req.POST['confirm_city']
            country = req.POST['confirm_country']
            shipping_method = req.POST['confirm_shipping_method']

            cart_products = UserProductVariantCart.objects.filter(user=req.user)
            shipping = ShippingMethod.objects.filter(id=shipping_method)[0]

            cart_total = 0

            for cart_product in cart_products:
                cart_total += cart_product.total()

            ## Create new Invoice instance
            new_invoice = Invoice()
            new_invoice.user = user
            new_invoice.shipping_method = shipping
            new_invoice.total_price = cart_total+shipping.price
            new_invoice.shipping_address = address
            new_invoice.shipping_city = city
            new_invoice.shipping_country = country
            new_invoice.save()

            ## Create the Invoice Products assigned to that Invoice
            for cart_product in cart_products:
                new_invoice_product = InvoiceProduct()
                new_invoice_product.invoice = new_invoice
                new_invoice_product.product = cart_product.product_variant
                new_invoice_product.quantity = cart_product.quantity
                new_invoice_product.save()

                ## Reduce the quantity in the database
                product = ProductVariant.objects.filter(id=cart_product.product_variant.id)[0]
                product.stock -= cart_product.quantity
                product.save()

            ## Empty the cart
            cart = UserProductVariantCart.objects.filter(user=user)
            cart.delete()

        else:
            print('the user is not logged in')

    context = {
        'email': email
    }

    return render(req, 'pages/products/confirmation.html', context)
