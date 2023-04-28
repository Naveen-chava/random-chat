from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

from auth.models import AuthToken


class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Token"
    model = AuthToken

    # overriding the authenticate_credentials method from the TokenAuthentication class
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related("user").get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_("Invalid token."))

        if token.is_expired():
            # delete the token and then raise exception
            token.delete()
            raise AuthenticationFailed(_("Token expired. Please login again."))

        if token.user.is_suspended:
            raise AuthenticationFailed(_("User account suspended."))

        if not token.user.is_active or token.user.is_deleted:
            raise AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)
