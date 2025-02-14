from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list():
    # You can also filter or modify the categories here if needed.
    return {'categories': Category.objects.all()}
