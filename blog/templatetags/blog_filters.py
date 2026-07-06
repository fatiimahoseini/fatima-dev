from django import template
from django.utils.safestring import mark_safe
from blog.models import ICON_SVG, ICON_COLORS

register = template.Library()


@register.filter(name="category_icon")
def category_icon(category):
    svg_paths = ICON_SVG.get(category.icon, ICON_SVG["list"])
    color = ICON_COLORS.get(category.icon, "text-white")
    return mark_safe(
        f'<svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 {color}" '
        f'fill="none" viewBox="0 0 24 24" stroke="currentColor">'
        f'{svg_paths}</svg>'
    )
