from http import HTTPStatus


def create_response_error(code, message, status_code):
    return {'code': code, 'message': message}, status_code


def create_validation_error(marshmallow_error):
    return (
        {
            'code': 'VALIDATION_ERROR',
            'message': 'Validation error',
            'errors': marshmallow_error.messages,
        },
        HTTPStatus.UNPROCESSABLE_ENTITY,
    )
