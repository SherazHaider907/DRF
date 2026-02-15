from django.db.models import Max
from django.shortcuts import render,get_object_or_404
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics


# function base view creating api

# def product_list(request):
#     products = Product.objects.all()
#     # if it single value wen dont have to right to many but if it more then one then we use many
#     serializer = ProductSerializer(products,many =True) 
#     return JsonResponse({
#         'data':serializer.data}
#     )


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products,many =True) 
#     return Response(serializer.data)

# # for primary key 
# @api_view(['GET'])
# def product_detail(request,pk):
#     product =get_object_or_404(Product,pk=pk)
#     serializer = ProductSerializer(product) 
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product').all()
#     serializer = OrderSerializer(orders,many =True) 
#     return Response(serializer.data)

# class base view

class ProductListAPiView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderListAPiView(generics.ListAPIView):
    queryset =  Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer




@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price= Max('price'))['max_price']
    })
    return Response(serializer.data)