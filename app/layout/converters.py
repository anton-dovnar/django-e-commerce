"""
Custom path converters
"""


class UnicodeSlugConverter:
    """
    Unicode slug converter.
    """

    regex = r'[-0-9_\w]+'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return f"{value}"
