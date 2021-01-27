from django.urls import path, register_converter

from layout.converters import UnicodeSlugConverter
from shop import views

register_converter(UnicodeSlugConverter, 'unislug')

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<unislug:category_slug>/', views.ProductListView.as_view(), name='product-list-by-category'),
    path('<int:id>/<unislug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
