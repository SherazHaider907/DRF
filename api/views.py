from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import (LimitOffsetPagination,
                                    PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product
from api.serializers import (OrderItemSerializer, OrderSerializer,
                            ProductInfoSerializer, ProductSerializer,OrderCreateSerializer)

from .filters import ProductFilter

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

# class UserOrderListAPiView(generics.ListAPIView):
#     queryset =  Order.objects.prefetch_related('items__product').all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)


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
    queryset =  Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
    @action(
            detail=False,
            methods=['get'],
            url_path='user-orders',
            )
    def user_order(self,request):
        orders = self.get_queryset().filter(user=request.user) 
        serializer = self.get_serializer(orders,many = True)
        return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
        'products':products,
        'count': len(products),
        'max_price':products.aggregate(max_price= Max('price'))['max_price']
    })
        return Response(serializer.data)

