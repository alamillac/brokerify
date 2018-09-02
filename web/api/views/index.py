from flask import current_app
from flask import request
from flask_restful import Resource
from web.api.views.security import login_required
from modules.logger import context
from app.models.core import Index
from web.api.serializer import IndexSchema


class IndexResource(Resource):
    @login_required
    def get(self, index_id=None):
        context.update_uuid()
        if index_id:
            current_app.logger.debug("Showing index %s", index_id)
            index = Index.get(index_id)
            response = IndexSchema().dump(index)
            return response.data, 200

        current_app.logger.debug("Showing all indices")
        indices = Index.all()
        response = IndexSchema(many=True).dump(indices)
        return response.data, 200
