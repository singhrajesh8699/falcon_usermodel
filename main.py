# -*- coding: utf-8 -*-

import falcon
import mimetypes
import os

from app import log
from app.middleware import JSONTranslator, DatabaseSessionManager, ResponseLogger , RedixDb, CorsMiddleware
from app.database import db_session, init_session
from app.api.common import base
from app.api.apiv1 import userauth,videocapture
from app.errors import AppError


LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        #self.add_route("app/api/apiv1/status", collections.Collection())
        self.add_route("/app/api/apiv1/login", userauth.Self())
        self.add_route("/app/api/apiv1/logout", userauth.Self())
        self.add_route("/app/api/apiv1/create_superadmin", userauth.Collection())
        self.add_route("/app/api/apiv1/create_user", userauth.Collection())
        self.add_route("/app/api/apiv1/create_group", userauth.Collection())
        self.add_route("/app/api/apiv1/update_records", userauth.Collection())
        self.add_route("/app/api/apiv1/delete_records", userauth.Collection())
        self.add_route("/app/api/apiv1/capture_video", videocapture.VideoCapture())
        self.add_route("/app/api/apiv1/stop_video", videocapture.VideoCapture())
        self.add_route("/app/api/apiv1/status", videocapture.VideoCapture())
        self.add_error_handler(AppError, AppError.handle)



init_session()
middleware = [JSONTranslator(), DatabaseSessionManager(db_session), ResponseLogger() , RedixDb(), CorsMiddleware()]

application = App(middleware=middleware)

'''def application(env, start_response):
        uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
        uwsgi.websocket_send("Hello world")
        while True:
                msg = uwsgi.websocket_recv()
                uwsgi.websocket_send(msg)'''

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 7000, application)
    httpd.serve_forever()
