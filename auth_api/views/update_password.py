from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.export_types.request_data_types.change_password import (
    ChangePasswordRequestType,
)
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from auth_api.services.user_services.user_services import UserServices


class UpdatePasswordView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                UserServices().change_password(
                    uid=user_id, request_data=ChangePasswordRequestType(**request.data)
                )
                return Response(
                    data={
                        "message": "Password updated successfully.",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
