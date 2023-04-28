import uuid
from typing import Union

from rest_framework.request import Request
from django.contrib.auth import authenticate, login, get_user_model
from django.core.validators import validate_email


from auth.models import AuthToken
from account.models import UserProfile
from account.api.serializers import UserProfileSerializer
from common.constants import UserGenderType, UserStatusType


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


def svc_account_logout_user(user: User) -> None:
    # Just deleting the auth token is enough for the logout
    user.auth_token.delete()


def _get_user_from_user_id(user_id: uuid.UUID) -> User:
    return User.objects.get(external_id=user_id)


def svc_account_update_user_profile(request_data: dict, user: User, serialized: bool = True) -> Union[User, dict]:
    # user = _get_user_from_user_id(user_id)

    if "name" in request_data:
        first_name = request_data["name"].get("first_name")
        last_name = request_data["name"].get("last_name")

        user.first_name = first_name
        user.last_name = last_name

    if "email" in request_data:
        validate_email(request_data["email"])  # throws validation error
        user.email = request_data["email"]

    if "is_active" in request_data:
        user.is_active = request_data["is_active"]

    if "password" in request_data:
        user.set_password(request_data["password"])

    if "gender" in request_data:
        user.user_profile.gender = UserGenderType.get_obj_for_string(request_data["gender"])  # throws key error

    if "status" in request_data:
        user.user_profile.status = UserStatusType.get_obj_for_string(request_data["status"])  # throws key error

    if "age" in request_data:
        user.user_profile.age = request_data["age"]

    user.user_profile.save()
    user.save()

    if serialized:
        return UserProfileSerializer(user.user_profile, many=False).data
    return user
