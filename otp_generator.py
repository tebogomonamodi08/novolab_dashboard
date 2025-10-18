import secrets


def generate_otp(length=6):
    otp =  ''.join(str(secrets.randbelow(10)) for _ in range(length))
    return otp
