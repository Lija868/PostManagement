
import jwt
from datetime import datetime
from django.conf import settings

format = "%Y-%m-%d %H:%M:%S"
jwtSecret = settings.JWT_SECRET
options = {
    'verify_exp': True
}


def jwtValidator(token):
    payLoad = jwt.decode(token, jwtSecret, algorithm="HS256", options=options)
    return payLoad
