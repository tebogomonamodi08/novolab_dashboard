import secrets

session = {}

def generator(email=None):
    lower_bound = 10**(6-1)
    upper_bound = 10**6-1
    range_otp = (upper_bound - lower_bound)+1
    otp = lower_bound + secrets.randbelow(range_otp)
    session[email]=otp
    return session

generator('tebogo@novolap.com')
print(session)