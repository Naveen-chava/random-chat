from django.contrib import admin
from .models import User, UserProfile

models = [User, UserProfile]
admin.site.register(models)
