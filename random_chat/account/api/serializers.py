from rest_framework import serializers

from account.models import User, UserProfile


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    email_verified = serializers.SerializerMethodField()
    is_suspended = serializers.SerializerMethodField()
    external_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "email_verified",
            "is_suspended",
            "first_name",
            "last_name",
            "external_id",
            "created",
            "modified",
        )

    def get_username(self, obj: User):
        return obj.get_username()

    def get_email(self, obj: User):
        return obj.get_email()

    def get_email_verified(self, obj: User):
        return obj.get_email_verified()

    def get_is_suspended(self, obj: User):
        return obj.get_is_suspened()

    def get_external_id(self, obj: User):
        return str(obj.get_external_id())


class UserProfileSerializer(serializers.ModelSerializer):
    user_account = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "user_account",
            "status",
            "gender",
            "age",
            "created",
            "modified",
            "auth_token",
        )

    def get_user_account(self, obj: UserProfile):
        return BaseUserSerializer(obj.user).data

    def get_status(self, obj: UserProfile):
        return obj.get_status()

    def get_gender(self, obj: UserProfile):
        return obj.get_gender()

    def get_auth_token(self, obj: UserProfile):
        return self.context.get("token")
