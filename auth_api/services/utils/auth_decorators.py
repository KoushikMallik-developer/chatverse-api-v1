from functools import wraps

from auth_api.auth_exceptions.user_exceptions import UserNotAuthenticatedError
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from auth_api.services.user_services.user_services import UserServices


def is_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        view, request = args
        user_id = decode_jwt_token(request=request)
        if validate_user_uid(uid=user_id).is_validated:
            request.user = UserServices().get_user_details(uid=user_id)
            return view_func(*args, **kwargs)
        raise UserNotAuthenticatedError()

    return _wrapped_view
