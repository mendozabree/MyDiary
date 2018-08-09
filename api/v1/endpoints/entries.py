"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import entry_creation_model, specific_entry, entry_get_model
from api.v1.database import Entry
from .users import authorizations


entry = Entry()
api.authorizations = authorizations


@api.route('/api/v1/entries')
class NewEntry(Resource):
    """Class for making a new entry"""

    @api.expect(entry_creation_model)
    @api.doc(security='api_key')
    @jwt_required
    def post(self):
        """Method to make new entry"""

        current_user = get_jwt_identity()
        new_entry_data = api.payload

        result = entry.new_entry(
            new_entry_data=new_entry_data,
            current_user=current_user)

        return result

    @jwt_required
    @api.doc(security='api_key')
    def get(self):
        """Method to get all entries"""
        current_user = get_jwt_identity()

        my_entries = entry.all_entries(current_user=current_user)

        return my_entries, 200


@api.route('/api/v1/entries/<int:entry_id>')
class GetSpecificEntry(Resource):
    """Class for retrieving specific entry"""

    @jwt_required
    def get(self, entry_id):
        """Method to get specific entry"""
        current_user = get_jwt_identity()
        output = entry.get_specific(entry_id=entry_id,
                                    current_user=current_user)
        return output

    @api.expect(entry_creation_model)
    @jwt_required
    def put(self, entry_id):
        """Method to update an entry"""
        modify_data = api.payload
        current_user = get_jwt_identity()

        response = entry.modify_entry(entry_id=entry_id,
                                      modify_data=modify_data,
                                      current_user=current_user)
        return response
