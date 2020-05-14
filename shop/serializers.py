from rest_framework import serializers
from .models import Invoice, InvoiceProduct, ProductVariant


class InvoiceProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = InvoiceProduct
      fields = ['product', 'quantity']


class InvoiceSerializer(serializers.ModelSerializer):

   invoice_products = InvoiceProductSerializer(many=True, read_only=True)

   class Meta:
      model = Invoice
      fields = ['id', 'transaction_datetime', 'total_price', 'shipping_method', 'shipping_address', 'shipping_city', 'shipping_country', 'status', 'invoice_products']