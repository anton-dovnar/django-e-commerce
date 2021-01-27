from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from shop.models import Category, Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        category = None
        categories = Category.objects.all()
        category_slug = self.kwargs.get('category_slug', None)
        products = self.model.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        self.extra_context = {
            'category': category,
            'categories': categories,
        }

        return products


class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True
