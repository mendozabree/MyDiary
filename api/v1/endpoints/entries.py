"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import entry_creation_model, entry_get_model
from api.v1.database import Entries


entry = Entries()


@api.route('/api/v1/entries')
class NewEntry(Resource):
    """Class for making a new entry"""
    @jwt_required
    @api.expect(entry_creation_model)
    def post(self):
        current_user = get_jwt_identity()
        new_entry_data = api.payload

        entry.new_entry(new_entry_data=new_entry_data, current_user=current_user)

        return 'Success', 201


@api.route('/api/v1/entries')
class RetrieveAll(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        my_entries = entry.all_entries(current_user=current_user)

        return my_entries, 200


@api.route('/api/v1/entries/<int:entry_id>')
class GetSpecificEntry(Resource):
    @jwt_required
    def get(self, entry_id):
        current_user = get_jwt_identity()
        output = Entries.get_specific_entry(entry_id=entry_id, current_user=current_user)
        if output:
            return output, 200
        else:
            return 'No entry found, check id', 404


@api.route('/api/v1/entries/<int:entry_id>')
class ModifyEntry(Resource):
    @jwt_required
    @api.expect(entry_creation_model)
    def put(self, entry_id):
        modify_data = api.payload
        current_user = get_jwt_identity()

        response = entry.modify_entry(entry_id=entry_id, modify_data=modify_data, current_user=current_user)
        return response
