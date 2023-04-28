from django.db import models
from django.contrib.auth.models import AbstractUser

from common.abstract_models import AbstractDateTimeStamp, AbstractExternalID, AbstractDelete
from common.constants import UserStatusType, UserGenderType


class User(AbstractUser, AbstractDateTimeStamp, AbstractExternalID, AbstractDelete):
    email = models.EmailField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):  # pragma: no cover
        return self.username

    class Meta:
        db_table = "user"

    def get_username(self) -> str:
        return self.username

    def get_email(self) -> str:
        return self.email

    def get_email_verified(self) -> bool:
        return self.email_verified

    def get_is_suspened(self) -> bool:
        return self.is_suspended

    @classmethod
    def create_user(
        cls,
        *,
        username: str,
        password: str,
        email: str = None,
        first_name: str = "",
        last_name: str = "",
    ) -> "User":
        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return user


class UserProfile(AbstractDateTimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    status = models.PositiveIntegerField(choices=UserStatusType.get_choices(), default=UserStatusType.OFFLINE.value)

    gender = models.PositiveIntegerField(
        choices=UserGenderType.get_choices(),
        default=UserGenderType.DO_NOT_WANT_TO_DISCOLSE.value,
    )

    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_status(self) -> str:
        return UserStatusType.get_string_for_value(self.status)

    def get_gender(self) -> str:
        return UserGenderType.get_string_for_value(self.gender)

    @classmethod
    def create_profile(cls, user, status=None, age=None, gender=None) -> "UserProfile":
        profile = cls(user=user)
        if status:
            profile.status = status
        if age:
            profile.age = age
        if gender:
            profile.gender = gender
        profile.save()
        return profile
