# apps/eol/throttles.py

from rest_framework.throttling import SimpleRateThrottle
from django.conf import settings


class DynamicScopeRateThrottle(SimpleRateThrottle):
    """
    A throttle that selects its rate based on a JWT claim 'throttle_scope'.
    - If no valid JWT is present: use scope = "anon"
    - If JWT is present: use scope = token["throttle_scope"] (one of "read" or "write")

    It then looks up the rate in settings.API_THROTTLE_RATES.
    The cache key is built manually as "<scope>:<identifier>" where identifier is:
      - the authenticated user's username for JWT users, or
      - the request IP address for anonymous users.
    """

    scope = "anon"

    def get_cache_key(self, request, view):
        """
        1) Determine which 'scope' to use:
             - If request.auth is None → scope = "anon"
             - Else → look at request.auth["throttle_scope"], default to "read" if missing or invalid
        2) Look up `self.rate = settings.API_THROTTLE_RATES[self.scope]`. If that rate is missing/None, return None to disable throttling.
        3) Build a unique key string combining scope + client identifier:
             - If user is authenticated (request.user.is_authenticated), use request.user.username
             - Otherwise, use self.get_ident(request) (which is typically the REMOTE_ADDR)
        4) Return that key so DRF can track counts under that key.
        """
        token = getattr(request, "auth", None)
        if not token:
            self.scope = "anon"
        else:
            chosen_scope = token.get("throttle_scope", "read")
            if chosen_scope not in settings.API_THROTTLE_RATES:
                chosen_scope = "read"
            self.scope = chosen_scope

        self.rate = settings.API_THROTTLE_RATES.get(self.scope)
        if not self.rate:
            return None

        if hasattr(request, "user") and request.user and request.user.is_authenticated:
            identifier = request.user.username
        else:
            identifier = self.get_ident(request)

        return f"{self.scope}:{identifier}"
