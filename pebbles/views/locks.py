from flask import Blueprint as FlaskBlueprint
from flask import abort
from flask_restful import marshal_with, fields

from pebbles.models import db, Lock
from pebbles.views.commons import auth
from pebbles.utils import requires_admin
from pebbles.server import restful


locks = FlaskBlueprint('locks', __name__)

lock_fields = {
    'lock_id': fields.String,
    'acquired_at': fields.DateTime
}


class LockView(restful.Resource):
    @auth.login_required
    @requires_admin
    @marshal_with(lock_fields)
    def put(self, lock_id):
        lock = Lock(lock_id)
        db.session.add(lock)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(409)
        return lock

    @auth.login_required
    def delete(self, lock_id):
        lock = Lock.query.filter_by(lock_id=lock_id).first()
        if not lock:
            abort(404)
        db.session.delete(lock)
        db.session.commit()
