from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import specific_entry
from api.v1.database import Entry

entry = Entry()


@api.route('/api/v1/entries/<int:entry_id>')
class GetSpecificEntry(Resource):
    """Class for retrieving specific entry"""

    @api.expect(specific_entry)
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
