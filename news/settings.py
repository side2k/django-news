from django.conf import settings
PUBLICATION_PLACES = getattr(settings, "PUBLICATION_PLACES", ())
settings.PUBLICATION_PLACES = PUBLICATION_PLACES