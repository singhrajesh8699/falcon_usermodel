# -*- coding: utf-8 -*-

import falcon
import json

from cerberus import Validator
from cerberus.errors import ValidationError

from app.errors import UnauthorizedError, InvalidParameterError

from auth import decrypt_token, verify_timed_token

FIELDS = {
    'username': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
    'role': {
        'type': 'list',
        'required': True,
        'allowed': ['sadmin','admin', 'user']
    },
    'goup_id' : {
        'type': 'list',
        'required': True,
    },
    'owner_id' : {
        'type': 'list',
        'required': True,
    },
    'phone': {
        'type': 'string',
        'regex': '[0-9]*',
    },
    'is_active' : {
        'type': 'integer',
        'required': True
    }
}

def validate_user_create(req, res, resource=None, params=None):
    schema = {
        'username': FIELDS['username'],
        'email': FIELDS['email'],
        'password': FIELDS['password'],
        'role':  FIELDS['role'],
        'phone': FIELDS['phone'],
        'is_active' : FIELDS['is_active']
    }
    
    v = Validator(schema)
    v.schema = {}
    v.allow_unknown = True
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)

def auth_required(req, res, resource=None, params=None):
    token = req.auth
    redixdb = req.context['redixdb']
    if redixdb.__contains__(token,'id'):
        time_token = decrypt_token(token)
        user_auth = verify_timed_token(time_token)
        if user_auth:
            return user_auth
        else:
            raise UnauthorizedError("auth required")
    else:
        raise UnauthorizedError("auth required")
        

def is_admin(req, res, resources):
    session = req.context['session']
    print "session :" , session
    print req, "is req *******"
    roles = json.loads(session.get("user_roles"))
    if not "admin" in roles:
        raise UnauthorizedError("Restricted access")
