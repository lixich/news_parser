from flask import jsonify

# TODO add errors
http_errors = {
    400: 'Bad request',
    404: 'Not found'
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
