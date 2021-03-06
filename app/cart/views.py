from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupon.forms import CouponApplyForm
from shop.models import Product


@require_POST
def cart_add(request, product_id):
    """
    Add product or update quantity in cart [[cart.py]].
    """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart-detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove product form cart [[cart.py]].
    """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if not cart.cart:
        cart.clear()

    return redirect('cart:cart-detail')


def cart_detail(request):
    """
    List cart items.
    Accept coupon for discount.
    """

    cart = Cart(request)

    if cart.cart:
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})

        coupon_form = CouponApplyForm()
        return render(request, 'cart/cart_detail.html', {'cart': cart, 'coupon_form': coupon_form})

    return redirect('shop:product-list')
