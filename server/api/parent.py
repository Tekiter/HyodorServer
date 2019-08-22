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
        pass
    
    @login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("relation", type=str, required=True)
        parser.add_argument("gender", type=str, required=False)
        parser.add_argument("birthday", type=str, default=True, required=False)

        args = parser.parse_args()

        

        user = get_user()

        if user == None:
            return {}, 401
        
        newinfo = ParentInfo()
        
        newinfo.set_column('name', args['name'])

        newinfo.set_column('relation', args['relation'])

        if args['gender']:
            newinfo.set_column('gender', args['gender'])
        if args['birthday']:
            try:
                dt = datetime.datetime.fromisoformat(args['datetime'])
                newinfo.set_enc_datetime('birthday', dt)
            except ValueError:
                return {'message':{'datetime': 'Wrong datetime format. It should be ISO 8601 format.'}}, 400
            
        
        newinfo.user = user

        db.session.add(newinfo)
        db.session.commit()

        return {}, 200




