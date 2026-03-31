from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """
    Safely get an attribute from an object.
    """
    if not obj:
        return ""
    
    # Handle callable attributes (like get_status_display)
    if hasattr(obj, f"get_{attr}_display"):
        return getattr(obj, f"get_{attr}_display")()
        
    val = getattr(obj, attr, "")
    if callable(val):
        return val()
    return val

@register.filter
def replace(value, arg):
    """
    Simple string replacement filter.
    """
    if not value:
        return ""
    parts = arg.split(",")
    if len(parts) != 2:
        return value.replace(arg, " ")
    return value.replace(parts[0], parts[1])

@register.filter
def get_label(form, field_name):
    """
    Get the label for a form field by name.
    """
    return form.fields.get(field_name).label if field_name in form.fields else field_name.replace("_", " ").capitalize()
