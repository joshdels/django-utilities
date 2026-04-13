from django.conf import settings
from rest_framework.throttling import AnonRateThrottle


class OnePerDayThrottle(AnonRateThrottle):
    scope = "one_per_day"

    def allow_request(self, request, view):
        if settings.DEBUG:
            return True

        return super().allow_request(request, view)
