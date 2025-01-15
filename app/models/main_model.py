from core.api_log import APILog
from sqlalchemy import inspect

class MainModel():

    FULL_FIELD_ACCESS_LEVEL = 'full access'

    REGISTERED_FIELD_ACCESS_LEVEL = 'registered only'

    OWNER_FIELD_ACCESS_LEVEL = 'owner only'

    # Define access levels for fields (to be overridden in child classes)
    restricted_fields = {}
        
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self):
        return "<%r>" % self.email
    
    def filter_fields(self, user=None):
        """
        Filter fields based on access level and the authenticated user.
        """
        user = user or getattr(g, 'current_user', None)  # Get the current user from Flask's global context
        is_authenticated = user is not None

        result = {}
        for field, access_level in self.restricted_fields.items():
            if access_level == self.FULL_FIELD_ACCESS_LEVEL:
                result[field] = getattr(self, field, None)
            elif access_level == self.REGISTERED_FIELD_ACCESS_LEVEL and is_authenticated:
                result[field] = getattr(self, field, None)
            elif access_level == self.OWNER_FIELD_ACCESS_LEVEL and is_authenticated and user.id == getattr(self, 'user_id', None):
                result[field] = getattr(self, field, None)
            else:
                APILog.log_warning(f"Attend to access to '{field}' field with {access_level} access level.")

        return result
    