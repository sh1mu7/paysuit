import pyotp


def generate_google_auth_key(user):
    return pyotp.totp.TOTP(user.otp_key).provisioning_uri(name=user.email, issuer_name='PaysuiteBD')


def verify_otp(user, otp):
    totp = pyotp.TOTP(user.otp_key)
    return totp.verify(otp)
