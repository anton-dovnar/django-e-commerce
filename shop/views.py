from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from cart.forms import CartAddProductForm
from shop.models import Category, Product


class ProductListView(ListView):
    model = Product
    paginate_by = 8

    def get_queryset(self):
        category = None
        category_slug = self.kwargs.get('category_slug', None)
        products = self.model.objects.list()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        self.extra_context = {
            'category': category,
        }

        return products

    def get(self, *args, **kwargs):
        object_list = self.get_queryset()
        paginator = self.get_paginator(object_list, self.paginate_by)

        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            page = 1

        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(page)
        except EmptyPage:
            if self.request.is_ajax():
                return HttpResponse('')

            object_list = paginator.page(paginator.num_pages)

        context = {
            'object_list': object_list,
            'offset': (page - 1) * self.paginate_by
        }

        if self.request.is_ajax():
            return render(self.request, 'shop/product_list_ajax.html', context)

        return super().get(self.request)


class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
