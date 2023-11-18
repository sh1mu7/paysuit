import random

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from coreapp.models import UserConfirmation, User


def get_client_info(request):
    """
    Returns ip address and user agent from request instance
    :param request: The original request instance
    :type request: HttpRequest
    :return: ip, user_agent
    :rtype: str, str
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    if not user_agent:
        user_agent = 'unknown'
    return ip, user_agent


def get_user_by_email(email):
    """
    Returns user instance by email
    :param email: email address of user
    :type email: str
    :return: user object if user exist other wise it will raise ObjectDoesNotExist error
    :rtype: User
    """
    return User.objects.get(email=email)


def get_user_by_mobile(mobile):
    """
    Returns user instance by mobile
    :param mobile: mobile of the user
    :type mobile: str
    :return: user object if user exist other wise it will raise ObjectDoesNotExist error
    :rtype: User
    """
    return User.objects.get(mobile=mobile)


def regenerate_token(user):
    """
    Regenerates token for user
    :param user: instance of User
    :type user: User
    :return: token, created
    :rtype: str, timestamp
    """
    token, created = Token.objects.get_or_create(user=user)
    if not created:
        token.delete()
    return Token.objects.get_or_create(user=user)


def validate_user(user):
    """
    Performs validation for user instance
    :param user: instance of user
    :type user: User
    :return:
    :rtype:
    """
    if not user.is_active:
        raise serializers.ValidationError({'email': [_("Your account has been disabled by administrator"), ]})


def validate_user_password(password):
    """
    Performs validation for user password
    :param password: password of the user
    :type password: str
    :return:
    :rtype:
    """
    try:
        validate_password(password)
    except ValidationError as e:
        raise serializers.ValidationError({'password': e.error_list})


def check_approval(user):
    """
    Performs approval validation for user instance
    :param user: instance of User
    :type user: User
    :return:
    :rtype:
    """
    if not user.is_approved:
        raise serializers.ValidationError({'email': [_("Your account has not been approved by yet"), ]})
