from django import template
from django.urls import reverse


register = template.Library()

@register.filter('input_type')
def input_type(obj):
    '''
    Extract form field type
    :param obj: form field
    :return: string of form field widget type
    '''
    return obj.field.widget.__class__.__name__
