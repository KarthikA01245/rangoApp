from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    """
    Returns a list of categories and highlights the current category (if passed).
    """
    categories = Category.objects.all()
    return {'categories': categories, 'current_category': current_category}
