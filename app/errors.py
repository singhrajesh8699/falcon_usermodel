# -*- coding: utf-8 -*-

import json
import falcon

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


OK = {
    'status': falcon.HTTP_200,
    'code': 200,
}

ERR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Unknown Error'
}

ERR_TABLE = {
    'status': falcon.HTTP_500,
    'code': 80,
    'title': 'Table Not Fount'
}

ERR_AUTH_REQUIRED = {
    'status': falcon.HTTP_401,
    'code': 99,
    'title': 'Authentication Required'
}

ERR_URL_FORBIDDEN = {
    'status': falcon.HTTP_403,
    'code': 403,
    'title': 'Url Not Found'
}

ERR_INVALID_PARAMETER = {
    'status': falcon.HTTP_400,
    'code': 88,
    'title': 'Invalid Parameter'
}

ERR_DATABASE_ROLLBACK = {
    'status': falcon.HTTP_500,
    'code': 77,
    'title': 'Database Rollback Error'
}

ERR_NOT_SUPPORTED = {
    'status': falcon.HTTP_404,
    'code': 10,
    'title': 'Not Supported'
}


ERR_USER_NOT_EXISTS = {
    'status': falcon.HTTP_200,
    'code': 21,
    'title': 'User Not Exists'
}

ERR_PASSWORD_NOT_MATCH = {
    'status': falcon.HTTP_200,
    'code': 22,
    'title': 'Password Not Match'
}


class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        meta = OrderedDict()
        meta['code'] = exception.code
        meta['message'] = exception.title
        resp = {
          "success": False
        }
        if exception.description:
            meta['description'] = exception.description
        res.body = json.dumps({'meta': meta, "data": resp})


class InvalidParameterError(AppError):
    def __init__(self, description=None):
        super(InvalidParameterError, self).__init__(ERR_INVALID_PARAMETER)
        self.error['description'] = description


class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super(DatabaseError, self).__init__(error)
        obj = OrderedDict()
        obj['details'] = ', '.join(args)
        obj['params'] = str(params)
        self.error['description'] = obj


class NotSupportedError(AppError):
    def __init__(self, method=None, url=None):
        super(NotSupportedError, self).__init__(ERR_NOT_SUPPORTED)
        if method and url:
            self.error['description'] = 'method: %s, url: %s' % (method, url)


class UserNotExistsError(AppError):
    def __init__(self, description=None):
        super(UserNotExistsError, self).__init__(ERR_USER_NOT_EXISTS)
        self.error['description'] = description


class PasswordNotMatch(AppError):
    def __init__(self, description=None):
        super(PasswordNotMatch, self).__init__(ERR_PASSWORD_NOT_MATCH)
        self.error['description'] = description


class UnauthorizedError(AppError):
    def __init__(self, description=None):
        super(UnauthorizedError, self).__init__(ERR_AUTH_REQUIRED)
        self.error['description'] = description


class UrlNotFound(AppError):
    def __init__(self, description=None):
        super(UrlNotFound, self).__init__(ERR_URL_FORBIDDEN)
        self.error['description'] = description


class TablelNotFound(AppError):
    def __init__(self, description=None):
        super(TablelNotFound, self).__init__(ERR_TABLE)
        self.error['description'] = description