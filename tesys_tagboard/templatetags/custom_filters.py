from django import template

register = template.Library()


@register.filter(name="concat")
def concat(value, arg) -> str:
    """Concatenate string value and arg string."""
    return f"{value}{arg}"


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key)
