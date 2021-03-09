import redis
from django.conf import settings

from shop.models import Product

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Recommender:
    def get_product_key(self, pk):
        return f'product:{pk}:purchased_with'

    def products_bought(self, products):
        product_pks = [p.pk for p in products]
        for product_pk in product_pks:
            for with_pk in product_pks:
                # Get the other products bought with each product
                if product_pk != with_pk:
                    # Increment score for product purchased together
                    r.zincrby(self.get_product_key(product_pk), 1, with_pk)

    def suggest_products_for(self, products, max_results=6):
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
        # Get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(pk__in=suggested_products_pks))
        suggested_products.sort(key=lambda x: suggested_products_pks.index(x.pk))
        return suggested_products

    def clear_purchases(self):
        for pk in Product.objects.values_list('pk', flat=True):
            r.delete(self.get_product_key(pk))
