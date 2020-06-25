from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Invoice
from .serializers import InvoiceSerializer
from .permissions import IsSuperUser


class InvoiceListAll(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceListConfirmed(generics.ListCreateAPIView):
    queryset = Invoice.objects.filter(status='Confirmed')
    serializer_class = InvoiceSerializer


class InvoiceListShipped(generics.ListCreateAPIView):
    queryset = Invoice.objects.filter(status='Shipped')
    serializer_class = InvoiceSerializer


@api_view(['GET', 'PUT'])
def InvoiceDetail(req, pk):

    if req.method == 'GET':
        queryset = Invoice.objects.filter(pk=pk)
        serializer_class = InvoiceSerializer(queryset, many=True)
        return Response(serializer_class.data)

    if req.method == 'PUT':
        new_status = req.data.get('status')

        queryset = Invoice.objects.get(id=pk)
        queryset.status = new_status
        queryset.save()

        return Response(queryset.status)
