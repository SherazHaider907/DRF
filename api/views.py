from django.shortcuts import render,get_object_or_404
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

# function base view creating api

# def product_list(request):
#     products = Product.objects.all()
#     # if it single value wen dont have to right to many but if it more then one then we use many
#     serializer = ProductSerializer(products,many =True) 
#     return JsonResponse({
#         'data':serializer.data}
#     )


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many =True) 
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request,pk):
    product =get_object_or_404(Product,pk=pk)
    serializer = ProductSerializer(product) 
    return Response(serializer.data)
