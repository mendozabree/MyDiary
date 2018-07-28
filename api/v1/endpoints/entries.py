"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.database import DatabaseConnection
from api.v1.serializers import entry_creation_model
from ..classes import Entries


@api.route('/api/v1/entries')
class NewEntry(Resource):

    @api.expect(entry_creation_model)
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        new_entry_data = api.payload

        new_entry = Entries(title=new_entry_data['title'],
                            content=new_entry_data['content'],
                            entry_date=new_entry_data['entry_date'],
                            entry_time=new_entry_data['entry_time'],
                            author=current_user
                            )
        new_entry.create_entry()

        return 'Success', 201
