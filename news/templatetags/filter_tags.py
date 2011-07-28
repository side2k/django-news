from django import template
register = template.Library()

@register.inclusion_tag('datetime_interval_filter.html')
def pub_place_interval_filter(cl, spec):
    return spec.get_output_dict(cl)