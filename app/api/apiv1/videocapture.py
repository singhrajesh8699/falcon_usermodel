import re
import falcon
import datetime
import json
from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required, validate_user_create
from app.utils.auth import encrypt_token, hash_password, verify_password, \
uuid, generate_timed_token, verify_timed_token, destroy_token
from app.model import User, Permission, Group_ , Owner, Base, IpCamera
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch, UrlNotFound, TablelNotFound

import threading ,sys, os
from multiprocessing.pool import ThreadPool

class VideoCapture(BaseResource):
    
    def __init__(self):
        self.camera = IpCamera()
        

    #@falcon.before(validate_user_create)
    def on_get(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == 'capture_video':
            res.stream = self.camera.gen(self.camera)
            res.status = falcon.HTTP_200
            res.content_type = 'multipart/x-mixed-replace; boundary=frame'

            '''user_auth=auth_required(req,res)
            session = req.context['db.session']
            email = user_auth['email']
            user_db = User.find_by_email(session, email)
            if user_db:
                user_req = req.context['data']
                camera = IpCamera()
                res.data = camera.gen(camera)
                res.status = falcon.HTTP_200
                res.content_type = 'multipart/x-mixed-replace; boundary=frame'
            else:
                raise UserNotExistsError('User email: %s' % email)'''
        
        elif cmd == 'status':
            res.status = falcon.HTTP_200
            res.body = "it is working"
        
        

    def on_post(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == 'stop_video':
            print 'stop_video'
            self.camera.destroy_thread()
            user_req = req.context['data']
            self.on_success(res, user_req)  
        

   





        
