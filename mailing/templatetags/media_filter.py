from django import template

register = template.Library()

@register.simple_tag
def mediapath(image_path):
    # Проверка, является ли image_path уже полным путем
    if image_path.startswith('/media/'):
        return image_path

    # Конкатенация '/media/' и image_path
    return '/media/' + image_path