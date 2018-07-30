"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.database import DatabaseConnection
from api.v1.serializers import entry_creation_model, entry_get_model
from ..classes import Entries


@api.route('/api/v1/entries')
class NewEntry(Resource):
    """Class for making a new entry"""
    @api.expect(entry_creation_model)
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        new_entry_data = api.payload

        new_entry = Entries(title=new_entry_data['title'],
                            content=new_entry_data['content'],
                            user_id=current_user
                            )
        new_entry.create_entry()

        return 'Success', 201


@api.route('/api/v1/entries')
class RetrieveAll(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        my_entries = Entries.retrieve_all_entries(user=current_user)

        return my_entries, 200


@api.route('/api/v1/entries/<int:entry_id>')
class GetSpecificEntry(Resource):
    @jwt_required
    def get(self, entry_id):
        output = Entries.get_specific_entry(entry_id=entry_id)
        if output:
            return output, 200
        else:
            return 'No entry found, check id', 400


@api.route('/api/v1/entries/<int:entry_id>')
class ModifyEntry(Resource):
    @jwt_required
    def put(self, entry_id):
        modify_data = api.payload
        current_user = get_jwt_identity()

        response = Entries.modify_entry(entry_id=entry_id, modify_data=
                                        modify_data, user=current_user)

        return response
