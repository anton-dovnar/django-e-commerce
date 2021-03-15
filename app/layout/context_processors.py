from shop.models import Category


def categories(request):
    """
    List available categories for sidebar.
    """

    # TODO cache query
    return {'categories': Category.objects.all()}
