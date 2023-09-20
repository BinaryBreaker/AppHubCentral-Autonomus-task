import random
import string


def genOtp(lent=4):
    otp = ''.join(random.choices(string.digits, k=lent))
    return otp
