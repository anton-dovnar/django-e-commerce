"""
Create backend aggregation recommender for purchases.
This aggregation depends on successful purchases, which items people often buy together.
Collect purchase data with Redis.
"""

import redis
from django.conf import settings

from shop.models import Product

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# === Recommender ===
class Recommender:
    """
    Recommender contains four main methods:

    - **get_product_key** product key for access data through Redis.
    - **products_bought** collect bought products.
    - **suggest_products_for** forming recommendations for a particular product [[views.py]].
    - **clear_purchases** clear collected data.
    """

    def get_product_key(self, pk):
        return f'product:{pk}:purchased_with'

    # ==== products_bought ====
    def products_bought(self, order):
        """
        - Get the other products bought with each product.
        - Increment score for product purchased together.
        """

        product_pks = [item.product.pk for item in order]
        for product_pk in product_pks:
            for with_pk in product_pks:
                if product_pk != with_pk:
                    r.zincrby(self.get_product_key(product_pk), 1, with_pk)

    # ==== suggest_products_for ====
    def suggest_products_for(self, products, max_results=6):
        """
        Get suggested products and sort by order of appearance.
        """

        product_pks = [p.pk for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_pks[0]), 0, -1, desc=True)[:max_results]
        else:
            # Generate a temporary key
            flat_pks = ''.join([str(pk) for pk in product_pks])
            tmp_key = f'tmp_{flat_pks}'
            # Multiple products, combine scores of all products
            # Store the resulting sorted set in a temporary key
            keys = [self.get_product_key(pk) for pk in product_pks]
            r.zunionstore(tmp_key, keys)
            # Remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_pks)
            # Get the product pks by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # Remove the temporary key
            r.delete(tmp_key)

        suggested_products_pks = [int(pk) for pk in suggestions]
        suggested_products = list(Product.objects.list().filter(pk__in=suggested_products_pks))
        suggested_products.sort(key=lambda x: suggested_products_pks.index(x.pk))
        return suggested_products

    # ==== clear_purchases ====
    def clear_purchases(self):
        """
        Clear recommendations.
        """

        for pk in Product.objects.values_list('pk', flat=True):
            r.delete(self.get_product_key(pk))
