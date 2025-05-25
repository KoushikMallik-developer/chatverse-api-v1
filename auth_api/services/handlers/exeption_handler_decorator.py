from functools import wraps

from auth_api.services.handlers.exception_handlers import ExceptionHandler


def handle_exceptions(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            # Handle the exception here
            # You can log the exception or return a custom response
            return ExceptionHandler().handle_exception(e)

    return _wrapped_view
