import datetime

from flask_restful import (reqparse, abort, Resource, fields, marshal)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required,
                                jwt_required, jwt_refresh_token_required)



from .. import db
from ..model import User, ParentInfo, ParentGroup
from ..services.login import login_required, permission_required, get_user, UserPermission




class ParentInfoManage(Resource):

    @login_required
    def get(self):
        user = get_user()

        items = ParentInfo.query.filter_by(user_id=user.id).all()
        print(items)

        outputlst = []

        i: ParentInfo
        for i in items:
            tmp = {
                'id': i.id,
                'relation': i.get_column('relation'),
                'name': i.get_column('name'),
                'gender': i.get_column('gender'),
                # 'birthday': i.get_enc_datetime('birthday').isoformat()
            }
            if i.birthday:
                tmp['birthday'] = i.get_enc_datetime('birthday').isoformat()
            else:
                tmp['birthday'] = None
            outputlst.append(tmp)


        return {
            'parents': outputlst
        }, 200
            
    
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("relation", type=str, required=True)
        parser.add_argument("gender", type=str, required=False)
        parser.add_argument("birthday", type=str, required=False)

        args = parser.parse_args()

        

        user = get_user()

        if user == None:
            return {}, 401
        
        newinfo = ParentInfo()
        
        newinfo.set_column('name', args['name'])

        newinfo.set_column('relation', args['relation'])

        if args.get('gender'):
            newinfo.set_column('gender', args['gender'])
        if args.get('birthday'):
            try:
                dt = datetime.datetime.fromisoformat(args['datetime'])
                newinfo.set_enc_datetime('birthday', dt)
            except ValueError:
                return {'message':{'datetime': 'Wrong datetime format. It should be ISO 8601 format.'}}, 400
            
        
        newinfo.user = user

        db.session.add(newinfo)
        db.session.commit()

        return {}, 200

    

class ParentInfoView(Resource):

    @login_required
    def get(self, parent_id):
        user = get_user()

        parent: ParentInfo = ParentInfo.query.get(parent_id)

        if parent == None:
            return {}, 404
        if parent.user != user:
            return {}, 403

        i = parent
        
        tmp = {
            'id': i.id,
            'relation': i.get_column('relation'),
            'name': i.get_column('name'),
            'gender': i.get_column('gender'),
            # 'birthday': i.get_enc_datetime('birthday').isoformat()
        }
        if i.birthday:
            tmp['birthday'] = i.get_enc_datetime('birthday').isoformat()
        else:
            tmp['birthday'] = None
        
        return tmp, 200

    @login_required
    def patch(self, parent_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("relation", type=str, required=True)
        parser.add_argument("gender", type=str, required=False)
        parser.add_argument("birthday", type=str, required=False)

        args = parser.parse_args()

        
        user = get_user()

        parent: ParentInfo = ParentInfo.query.get(parent_id)

        if parent == None:
            return {}, 404
        if parent.user != user:
            return {}, 403
        
        newinfo = parent
        
        newinfo.set_column('name', args['name'])

        newinfo.set_column('relation', args['relation'])

        if args.get('gender'):
            newinfo.set_column('gender', args['gender'])
        if args.get('birthday'):
            try:
                dt = datetime.datetime.fromisoformat(args['datetime'])
                newinfo.set_enc_datetime('birthday', dt)
            except ValueError:
                return {'message':{'datetime': 'Wrong datetime format. It should be ISO 8601 format.'}}, 400
            
        db.session.commit()

        return {}, 200

    @login_required
    def delete(self, parent_id):
        user = get_user()

        parent: ParentInfo = ParentInfo.query.get(parent_id)

        if parent == None:
            return {}, 404
        if parent.user != user:
            return {}, 403
        
        db.session.delete(parent)
        db.session.commit()

        return {}, 200
        



class ParentGroupManage(Resource):

    @login_required
    def get(self):
        user = get_user()

        groups = user.parentgroups

        output = []

        i: ParentGroup
        for i in groups:
            tmp = {
                'id': i.id,
                'name': i.name,
                'prefer_call': i.prefer_call,
                'prefer_visit': i.prefer_visit
            }
            output.append(tmp)
        
        return {
            'groups': output
        }, 200

    @login_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("prefer_call", type=int, required=False)
        parser.add_argument("prefer_visit", type=int, required=False)

        args = parser.parse_args()

        user = get_user()

        newgroup = ParentGroup()
        newgroup.name = args['name']
        newgroup.prefer_call = args['prefer_call']
        newgroup.prefer_visit = args['prefer_visit']

        newgroup.user = user

        db.session.add(newgroup)
        db.session.commit()

        return {}, 201