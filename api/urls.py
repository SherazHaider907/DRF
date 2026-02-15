from django.urls import path
from . import views

urlpatterns = [
    # path('products/',views.product_list), fun
    path('products/',views.ProductListAPiView.as_view()),
    path('products/info/',views.product_info),
    # path('products/<int:pk>/',views.product_detail), fun
    path('products/<int:product_id>/',views.ProductDetailAPIView.as_view()),
    path('orders/',views.OrderListAPiView.as_view()),
    path('user-orders/',views.UserOrderListAPiView.as_view(),name='user-orders'),
]
