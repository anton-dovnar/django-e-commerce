"""
Currently support the follow two views:

1. **Product List** - list available products [[views.py#list]].
2. **Product Detail** - detail product page [[views.py#detail]].
"""

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from cart.forms import CartAddProductForm
from shop.models import Category, Product
from shop.recommender import Recommender


# === List ===
class ProductListView(ListView):
    model = Product
    paginate_by = 8

    def get_queryset(self):
        """
        Filter products by Category.
        """

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

    def render_to_response(self, context, **response_kwargs):
        """
        Infinite scroll with ajax request.
        """

        if self.request.is_ajax():
            return render(self.request, 'shop/product_list_ajax.html', context)

        return super().render_to_response(context, **response_kwargs)


# === Detail ===
class ProductDetailView(DetailView):
    model = Product
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        """
        Add product to cart.
        Suggest products for this product [[recommender.py#suggest_products_for]].
        """

        context = super().get_context_data(**kwargs)
        product = super().get_object()
        r = Recommender()
        context['cart_product_form'] = CartAddProductForm()
        context['recommended_products'] = r.suggest_products_for([product], 4)
        return context
