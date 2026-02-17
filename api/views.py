from django.db.models import Max
from django.shortcuts import render,get_object_or_404
from api.serializers import ProductSerializer,OrderSerializer,OrderItemSerializer,ProductInfoSerializer
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated ,IsAdminUser,AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets
from .filters import ProductFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import ProductFilter,InStockFilterBackend
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
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

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products':products,
#         'count': len(products),
#         'max_price':products.aggregate(max_price= Max('price'))['max_price']
#     })
#     return Response(serializer.data)



# class :
    # class ProductCreateAPiView(generics.CreateAPIView):
#     model  = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)
# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = 'product_id'

# generics views
# class OrderListAPiView(generics.ListAPIView):
#     queryset =  Order.objects.prefetch_related('items__product').all()
#     serializer_class = OrderSerializer


# class base view

class ProductListCreateAPiView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    # filterset_fields = ('name','price')
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
        ]
    search_fields = ['name', 'description']
    ordering_fields = ['name','price','stock']
    pagination_class  = LimitOffsetPagination
    # pagination_class  = PageNumberPagination
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

class OrderViewset(viewsets.ModelViewSet):
    queryset =  Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None

# class UserOrderListAPiView(generics.ListAPIView):
#     queryset =  Order.objects.prefetch_related('items__product').all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)
        
        


class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price= Max('price'))['max_price']
    })
        return Response(serializer.data)

