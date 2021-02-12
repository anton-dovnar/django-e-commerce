from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('create/', views.OrderFormView.as_view(), name='order-create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin-order-detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin-order-pdf'),
]
