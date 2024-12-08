from django import template

register = template.Library()

@register.filter
def exclude_user(queryset, user):
    return queryset.exclude(id=user.id)