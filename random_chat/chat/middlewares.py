# from rest_framework.authtoken.models import Token
# from urllib.parse import parse_qs
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser


# @database_sync_to_async
# def returnUser(token_string):
# 	try:
# 		user = Token.objects.get(key=token_string).user
# 	except:
# 		user = AnonymousUser()
# 	return user


# class TokenAuthMiddleWare:
# 	def __init__(self, app):
# 		self.app = app

# 	async def __call__(self, scope, receive, send):
# 		query_string = scope["query_string"]
# 		query_params = query_string.decode()
# 		query_dict = parse_qs(query_params)
# 		token = query_dict["token"][0]
# 		user = await returnUser(token)
# 		scope["user"] = user
# 		return await self.app(scope, receive, send)

from auth.models import AuthToken
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, AnonymousUser
from channels.db import database_sync_to_async

'''
@database_sync_to_async
def get_user(token):
    try:
        # return User.objects.get(id=user_id)
        return AuthToken.objects.get(key=token).user
    # except User.DoesNotExist:
    except AuthToken.DoesNotExist:
        return AnonymousUser()

class CustomAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        # scope['user'] = await get_user(int(scope["query_string"]))
        print("\n\n", scope, receive, send, "\n\n")
        print("\n\n", type(scope))
        print("\n\n", scope, "\n\n")
        print("\n\n", scope["headers"], "\n\n")
        # print("\n\n", scope.headers.get("authorization"), "\n\n")
        authorization = None
        for header in scope['headers']:
            if header[0].decode() == 'authorization': # the values in header are bytes type, so using decode() to convert them to a regular string
                authorization = header[1].decode()
                break
        # scope['user'] = await get_user(str(scope["Authorization"]))
        scope['user'] = await get_user(authorization)

        return await self.app(scope, receive, send)
    
'''


from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from auth.auth_class import CustomTokenAuthentication


@database_sync_to_async
def get_user(token):
    user, _ = CustomTokenAuthentication().authenticate_credentials(token)
    return user or AnonymousUser()

class CustomAuthMiddleware:
    """
    Custom middleware that authenticates WebSocket connections using token authentication.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        try:
            authorization = None
            for header in scope['headers']:
                if header[0].decode() == 'authorization': # the values in header are bytes type, so using decode() to convert them to a regular string
                    authorization = header[1].decode().split()[1]
                    break
            # scope['user'] = await get_user(str(scope["Authorization"]))
            scope['user'] = await get_user(authorization)
        except (IndexError, TypeError):
                scope['user'] = SimpleLazyObject(lambda: AnonymousUser())


        # authorization = get_authorization_header(scope)
        # if not authorization:
        #     scope['user'] = SimpleLazyObject(lambda: AnonymousUser())
        # else:
        #     try:
        #         token = authorization.decode().split()[1]
        #         scope['user'] = await get_user(token)
        #     except (IndexError, TypeError, AuthenticationFailed):
        #         scope['user'] = SimpleLazyObject(lambda: AnonymousUser())

        return await self.app(scope, receive, send)
