from .broker_utils import publish_event


def user_signup(user, user_confirmation):
    data = {
        'uid': str(user.uid),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'mobile': user.mobile,
        'fcm_key': user.fcm_key,
        'method': user.otp_method,
        'otp': {
            'uid': str(user_confirmation.uid),
            'code': user_confirmation.confirmation_code,
            'ip_address': user_confirmation.ip_address,
        }
    }
    publish_event('user_signup', data)


def user_login(user, user_confirmation):
    data = {
        'uid': str(user.uid),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'mobile': user.mobile,
        'fcm_key': user.fcm_key,
        'method': user.otp_method,
        'otp': None
    }
    if user_confirmation:
        otp = {
            'uid': str(user_confirmation.uid),
            'code': user_confirmation.confirmation_code,
            'ip_address': user_confirmation.ip_address
        }
        data['otp']: otp
    publish_event('user_login', data)


def user_updated():
    pass


def user_password_changed():
    pass


def user_verified():
    pass


def user_approved():
    pass


def user_deactivated():
    pass


def user_deleted():
    pass


def user_perm_updated():
    pass
