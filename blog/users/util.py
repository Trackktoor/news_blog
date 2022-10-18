from django.conf import settings
from django.core.mail import send_mail
import cryptocode
from blog.secrets import KEY_FOR_HASH

import random

def send_verify_mail(mail):
    verify_code = round((random.random())*10000)
    mail = send_mail('Регситрация на сайте NewsBlog!', str(verify_code), settings.EMAIL_HOST_USER, [mail])

    hash_verify_code = cryptocode.encrypt(str(verify_code), KEY_FOR_HASH)

    return {"status": mail, "hash_verify_code": hash_verify_code}