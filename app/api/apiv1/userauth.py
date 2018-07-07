# -*- coding: utf-8 -*-

import re
import falcon
import datetime
import json

from sqlalchemy.orm.exc import NoResultFound

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required, validate_user_create
from app.utils.auth import encrypt_token, hash_password, verify_password, \
uuid, generate_timed_token, verify_timed_token, destroy_token
from app.model import User, Permission, Group_ ,Owner,Base
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch, UrlNotFound, TablelNotFound

LOG = log.get_logger()

#import ipdb; ipdb.set_trace()

class Collection(BaseResource):
    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]

        if cmd == 'create_superadmin':
            session = req.context['db.session']
            user_req = req.context['data']
            if user_req:
                user = User()
                user.username = user_req['username']
                user.email = user_req['email']
                user.password = hash_password(user_req['password']).decode('utf-8')
                user.phone = user_req['phone'] if 'phone' in user_req else None
                user.is_active = user_req['is_active']
                session.add(user)
                roles = user_req['role']
                for role in roles:
                    permission = Permission.find_by_name(session, role)
                    if not permission:
                        permission = Permission()
                        permission.name = role
                        session.add(permission)
                    permission.User.append(user)
                self.on_success(res, user_req)    
            else:
                raise InvalidParameterError(req.context['data'])

        elif cmd == 'create_user':
            user_auth=auth_required(req,res)
            session = req.context['db.session']
            email = user_auth['email']
            user_db = User.find_by_email(session, email)
            if user_db:
                user_req = req.context['data']
                if user_req:
                    user = User()
                    user.username = user_req['username']
                    user.email = user_req['email']
                    user.password = hash_password(user_req['password']).decode('utf-8')
                    user.phone = user_req['phone'] if 'phone' in user_req else None
                    user.is_active = user_req['is_active']
                    session.add(user)

                    roles = user_req['role']
                    for role in roles:
                        permission = Permission.find_by_name(session, role)
                        if not permission:
                            permission = Permission()
                            permission.name = role
                            session.add(permission)
                        permission.User.append(user)

                    group_id = user_req['group_id']
                    for gid in group_id:
                        group = Group_.get_id(session, gid)
                        if group:
                            group.User.append(user)
                    
                    owners = user_req['owner_id']
                    for owner_id in owners:
                        owner = Owner.get_id(session, owner_id)
                        if not owner:
                            owner = Owner()
                            owner.owner_id=owner_id
                            session.add(owner)
                        owner.User.append(user)

                    self.on_success(res, user_req)
                else:
                    raise InvalidParameterError(req.context['data'])
            else:
                raise UserNotExistsError('User email: %s' % email)

        elif cmd == 'create_group':
            session = req.context['db.session']
            user_auth=auth_required(req,res)
            email = user_auth['email']
            user_db = User.find_by_email(session, email)
            if user_db:
                grp_req = req.context['data']
                if grp_req:
                    group = Group_()
                    group.name = grp_req['name']
                    group.email = grp_req['email']
                    group.size = grp_req['size'] 
                    session.add(group)
                    group.User.append(user_db)  
                    self.on_success(res, grp_req)
                else:
                    raise InvalidParameterError(req.context['data'])
            else:
                raise UserNotExistsError('User email: %s' % email)
        
        elif cmd == 'update_records':
            session = req.context['db.session']
            user_auth=auth_required(req,res)
            email = user_auth['email']
            user_db = User.find_by_email(session, email)
            if user_db:
                user_req = req.context['data']
                TableClass=Base().get_class_by_tablename(user_req['table_name'])
                if TableClass == None: 
                    raise TablelNotFound("Table %s not found" % user_req['table_name'])
                TableObject = {k:v for k, v in user_req.items() if k!= 'table_name'}
                session.query(TableClass).filter_by(email=user_req['email']).update(TableObject)
                self.on_success(res, {'status':'updated'})
            else:
                raise UserNotExistsError('User email: %s' % email)
        
        elif cmd == 'delete_records':
            session = req.context['db.session']
            user_auth=auth_required(req,res)
            email = user_auth['email']
            user_db = User.find_by_email(session, email)
            if user_db:
                user_req = req.context['data']
                TableClass=Base().get_class_by_tablename(user_req['table_name'])
                if TableClass == None: 
                    raise TablelNotFound("Table %s not found" % user_req['table_name'])
                session.query(TableClass).filter_by(email=user_req['email']).delete()
                self.on_success(res, {'status':'deleted'})
            else:
                raise UserNotExistsError('User email: %s' % email)

        else:
            raise UrlNotFound(req.context['data'])


    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['db.session']
        user_dbs = session.query(User).all()
        if user_dbs:
            obj = [user.to_dict() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Status(BaseResource):
    """
    Handle for endpoint: /api/status
    """
    def on_get(self, req, res):
       session = req.context['session']
       authenticated = session.get("authenticated")
       #checking the user authenticted  in session data
       status = False
       roles = []
       user_name = ""
       if authenticated == "True":
          status = True
          roles = json.loads(session.get("user_roles"))
          user_name = session.get("user_name")
       self.on_success(res, {"status": status, "roles": roles, "username": user_name})



class Self(BaseResource):
    """
    Handle for endpoint: /app/api/apiv1/login
    Handle for endpoint: /app/api/apiv1/logout
    """
    def on_post(self, req, res):
        db_session = req.context['db.session']
        redixdb = req.context['redixdb']
        user_req = req.context['data']
        email = None
        if user_req:
            email = user_req['email']
            password = user_req['password']
            try:
                # verifying user credentials
                user_db = User.find_by_email(db_session, email)
                user_id = user_db.id
                user_name = user_db.username
                roles = [i.name for i in user_db.permissions]
                if verify_password(password, user_db.password.encode('utf-8')):
                    user_data = user_db.to_dict()
                    for item in ["password", "created", "modified"]:
                        del user_data[item]
                    user_data["roles"] = roles
                    #creating token
                    timed_token = generate_timed_token(user_data)
                    token = encrypt_token(timed_token)
                    redixdb.set_hashkey(token,user_id)
                    res.set_header('token', token)
                    user_data["success"] = True
                    self.on_success(res, user_data)
                else:
                    raise PasswordNotMatch()
            except NoResultFound:
                raise UserNotExistsError('User email: %s' % email)

    @falcon.before(auth_required)
    def on_get(self, req, res):
        status = destroy_token(req)
        self.on_success(res, {"success": status})

    @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass
