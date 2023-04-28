from rest_framework.throttling import AnonRateThrottle

class TokenLessAPIThrottle(AnonRateThrottle):
    """
    To be used by Auth APIs: Login, Signup
    """
    scope = "token_less_auth_api_throttle"
