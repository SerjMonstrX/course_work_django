from django.core.cache import cache
from django.conf import settings
from .models import Mailing


def get_mailings():
    if settings.CACHE_ENABLED:
        mailings = cache.get('mailings')
        if not mailings:
            mailings = list(Mailing.objects.all())
            cache.set('mailings', mailings)
    else:
        mailings = list(Mailing.objects.all())
    return mailings
