from typing import Union, List

from rest_framework.request import Request
from django.contrib.auth import authenticate, login, logout, get_user_model

from auth.models import AuthToken
from account.models import UserProfile
from account.api.serializers import UserProfileSerializer


User = get_user_model()


def svc_account_create_user(request_data: dict, serialized: bool = True) -> Union[UserProfile, dict]:
    if "username" not in request_data:
        raise ValueError("Username missing in the request data")
    if "password" not in request_data:
        raise ValueError("Password missing in the request data")

    username = request_data["username"]
    password = request_data["password"]
    email = request_data.get("email", None)
    first_name = request_data.get("first_name", "")
    last_name = request_data.get("last_name", "")

    # create user
    user = User.objects.create_user(
        username=username, email=email, password=password, first_name=first_name, last_name=last_name
    )
    user.save()

    # create user profile
    profile = UserProfile.create_profile(user=user)

    if serialized:
        return UserProfileSerializer(profile, many=False).data
    return profile


def _get_or_create_user_token(user: User) -> str:
    try:
        token = AuthToken.objects.get(user=user)
    except AuthToken.DoesNotExist:
        token = AuthToken.create_token(user=user)

    return token.key


def svc_account_login_user(request: Request, serialized: bool = True) -> Union[str, dict]:
    request_data = request.data

    if "username" not in request_data:
        raise ValueError("Username missing in the request data")
    if "password" not in request_data:
        raise ValueError("Password missing in the request data")

    username = request_data["username"]
    password = request_data["password"]

    user = authenticate(username=username, password=password)

    if not user:
        raise ValueError("Invalid username or password")

    login(request, user)

    token = _get_or_create_user_token(user)

    if serialized:
        return UserProfileSerializer(user.user_profile, context={"token": token}, many=False).data
        # User object has an OneToOne relation with UserProfile object, so we can use user.user_profile
    return token


def svc_account_logout_user(request: Request) -> None:
    # delete auth token and then logout
    request.user.auth_token.delete()
    logout(request)
