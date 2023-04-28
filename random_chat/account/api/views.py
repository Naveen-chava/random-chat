from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.throttlers import TokenLessAPIThrottle
from common.auth_class import CustomTokenAuthentication
from services.account import (
    svc_account_create_user,
    svc_account_login_user,
    svc_account_logout_user,
    svc_account_update_user_profile,
)


User = get_user_model()


class UserSignupView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [TokenLessAPIThrottle]

    def post(self, request, **kwargs):
        try:
            return Response(svc_account_create_user(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [TokenLessAPIThrottle]

    def post(self, request, **kwargs):
        try:
            return Response(svc_account_login_user(request), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        svc_account_logout_user(request.user)
        return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, **kwargs):
        try:
            return Response(svc_account_update_user_profile(request.data, request.user), status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"message": f"Invalid Gender - {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
