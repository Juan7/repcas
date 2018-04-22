"""Template tags for report project."""

from django.template.defaulttags import register


@register.filter(name='lookup')
def lookup(dictionary, key):
    """Get a value from a dictionary given the key on templates."""
    res = dictionary.get(key, False)
    return res


@register.filter
def add_placeholder(field, placeholder=None):
    """Set placeholder on form input."""
    placeholder = field.field.widget.attrs.get('placeholder')
    if placeholder:
        field.field.widget.attrs.update({'placeholder': placeholder})
    else:
        field.field.widget.attrs.update({'placeholder': field.label})
    return field
