from flask import jsonify

http_errors = {
    400: 'Bad request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not found',
    500: 'Internal Server Error'
}


def generate_error(code, message=None):
    error = {}
    if code in http_errors:
        error['error'] = http_errors[code]
        if message:
            error['message'] = message
        return jsonify(error), code
    else:
        raise Exception('Incorrect code error', code)
