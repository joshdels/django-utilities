from django.conf import settings
from rest_framework.throttling import AnonRateThrottle


class OnePerDayThrottle(AnonRateThrottle):
    scope = "one_per_day"
