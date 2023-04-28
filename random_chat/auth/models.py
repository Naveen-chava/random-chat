from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token


class AuthToken(Token):
    expires_at = models.DateTimeField()

    @classmethod
    def create_token(cls, user):
        token = cls(user=user)
        token.expires_at = timezone.now() + timezone.timedelta(days=settings.TOKEN_EXPIRY_DAYS)

        token.save()
        return token

    def is_expired(self):
        return timezone.now() > self.expires_at
