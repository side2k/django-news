from django.conf import settings
PUBLICATION_PLACES = getattr(settings, "PUBLICATION_PLACES", ())
