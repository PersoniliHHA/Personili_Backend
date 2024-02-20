from rest_framework.permissions import BasePermission
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class IsAuthenticatedWithJWT(BasePermission):
    def has_permission(self, request, view):
        # Check if the JWT token is present in the request headers
        if 'Authorization' not in request.headers:
            return False

        # Extract the JWT token from the Authorization header
        auth_header = request.headers['Authorization']
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) == 2 else None

        # Check if the JWT token is valid and authenticated
        jwt_authentication = BaseJSONWebTokenAuthentication()
        user, token = jwt_authentication.authenticate_credentials(token)

        # Return True if the token is authenticated, False otherwise
        return user is not None
