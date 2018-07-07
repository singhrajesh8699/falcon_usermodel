# -*- coding: utf-8 -*-

import bcrypt
import shortuuid
import time
import datetime

from itsdangerous import TimedSerializer
from itsdangerous import SignatureExpired, BadSignature
from cryptography.fernet import Fernet, InvalidToken

from app.config import SECRET_KEY, UUID_LEN, UUID_ALPHABET

app_secret_key = Fernet(SECRET_KEY)

TOKEN_EXPIRES = 3600

def get_common_key():
    return app_secret_key


def uuid():
    return shortuuid.ShortUUID(alphabet=UUID_ALPHABET).random(UUID_LEN)

def encrypt_token(data):
        encryptor = get_common_key()
        return encryptor.encrypt(data.encode('utf-8'))


def decrypt_token(token):
    try:
        decryptor = get_common_key()
        return decryptor.decrypt(token.encode('utf-8'))
    except InvalidToken:
        return None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed


def generate_timed_token(user_dict):
    s = TimedSerializer(SECRET_KEY)
    return s.dumps(user_dict)


def verify_timed_token(token):
    s = TimedSerializer(SECRET_KEY)
    print "verify_timed_token" , TOKEN_EXPIRES
    try:
        data = s.loads(token,max_age=TOKEN_EXPIRES)
    except (SignatureExpired, BadSignature):
        return None
    return data

def destroy_token(req):
    token = req.auth
    redixdb = req.context['redixdb']
    redixdb.destroykey(token,'id')
    return True

