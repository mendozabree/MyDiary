"""This is the entries module

This module contains the entries endpoints
"""

from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import entry_creation_model, specific_entry
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
    @jwt_required
    def get(self):
        """Method to get all entries"""
        current_user = get_jwt_identity()

        my_entries = entry.all_entries(current_user=current_user)

        return {'message': my_entries}, 200


@api.route('/api/v1/entries/<int:entry_id>')
class GetSpecificEntry(Resource):
    """Class for retrieving specific entry"""

    @api.marshal_with(specific_entry, envelope='resource')
    @jwt_required
    def get(self, entry_id):
        """Method to get specific entry"""
        current_user = get_jwt_identity()
        output = entry.get_specific(entry_id=entry_id,
                                    current_user=current_user)
        if output:

            return {'message': output}, 200
        else:
            return {'message': 'No entry found, check id'}, 404


@api.route('/api/v1/entries/<int:entry_id>')
class ModifyEntry(Resource):
    """Class to modify all entries"""

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