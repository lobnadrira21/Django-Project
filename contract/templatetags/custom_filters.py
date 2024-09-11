from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if isinstance(value, BoundField):  # Vérifiez que 'value' est bien un champ de formulaire
        return value.as_widget(attrs={'class': arg})
    return value  # Si ce n'est pas un champ, retournez simplement la valeur telle quelle
