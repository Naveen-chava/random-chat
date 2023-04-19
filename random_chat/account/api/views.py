from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from auth.auth_class import CustomTokenAuthentication
from services.account import svc_account_create_user, svc_account_login_user, svc_account_logout_user


class UserSignupView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            return Response(svc_account_create_user(request_data=request.data), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            return Response(svc_account_login_user(request), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        svc_account_logout_user(request)
        return Response({"message": "User logged out successfully."}, status=status.HTTP_204_NO_CONTENT)
