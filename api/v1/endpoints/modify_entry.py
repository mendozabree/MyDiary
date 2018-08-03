from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from api import api
from api.v1.serializers import modify_entry
from api.v1.database import Entry


entry = Entry()


@api.route('/api/v1/entries/<int:entry_id>')
class ModifyEntry(Resource):
    """Class to modify all entries"""

    @api.expect(modify_entry)
    @jwt_required
    def put(self, entry_id):
        """Method to update an entry"""
        modify_data = api.payload
        current_user = get_jwt_identity()

        response = entry.modify_entry(entry_id=entry_id,
                                      modify_data=modify_data,
                                      current_user=current_user)
        return response