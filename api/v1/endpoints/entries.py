"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import entry_creation_model, entry_get_model
from api.v1.database import Entry


entry = Entry()


@api.route('/api/v1/entries')
class NewEntry(Resource):
    """Class for making a new entry"""

    @api.expect(entry_creation_model)
    @jwt_required
    def post(self):
        """Method to make new entry"""

        current_user = get_jwt_identity()
        new_entry_data = api.payload

        result = entry.new_entry(
            new_entry_data=new_entry_data,
            current_user=current_user)

        return result


@api.route('/api/v1/entries')
class RetrieveAll(Resource):
    """Class for retrieving all user entries"""

    @api.marshal_with(entry_get_model)
    @jwt_required
    def get(self):
        """Method to get all entries"""
        current_user = get_jwt_identity()

        my_entries = entry.all_entries(current_user=current_user)

        return {'message': my_entries}, 200
