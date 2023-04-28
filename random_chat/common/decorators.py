############################  DEPRECATED  ############################
# Used it in the first version but now using CustomTokenAuthentication class which can perform the same operations
# This decorator may not work in future due to changes in other apps/functions


from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from auth.models import AuthToken
from account.models import User
from services.account import svc_account_logout_user


def validate_profile(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        token = AuthToken.objects.get(key=request.META.get("HTTP_AUTHORIZATION", "").split()[1])
        if token.is_expired():
            svc_account_logout_user(request)
            return Response({"message": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)

        user_account: User = token.user
        if user_account.get_is_suspened():
            return Response({"message": "Account suspended"}, status=status.HTTP_403_FORBIDDEN)

        if user_account.is_deleted:
            return Response({"message": "Account deleted"}, status=status.HTTP_403_FORBIDDEN)

        kwargs["user"] = user_account

        return func(self, request, *args, **kwargs)

    return wrapper
