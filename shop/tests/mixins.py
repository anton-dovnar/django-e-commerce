from shop.models import Category, Product


class SetUpMixin:
    """
    Create Fixtures for testing.
    """

    def setUp(self):
        self.category = Category(name='Shoes', slug='shoes')
        self.category.save()

        self.product = Product(
            category=self.category, name='Nike SB Zoom Blazer Mid Edge',
            slug='nike-sb-zoom-blazer-mid-edge',
            description="""Want a custom look without the elbow grease?
            The Nike SB Zoom Blazer Mid Edge adds that something extra
            to your kicks with DIY details like frayed stitching, cut-out
            eyestays and patches of extra material in high-wear areas.""",
            price=89.95, available=True
        )
        self.product.save()
