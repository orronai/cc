from flask import abort, jsonify


class CurrenciesError(Exception):
    pass


class CurrencyError(CurrenciesError):
    pass


class DateError(CurrenciesError):
    pass


# Credit to Yam Mesicka
# https://github.com/PythonFreeCourse/lms/blob/master/lms/models/errors.py#L40
def fail(status_code: int, error_msg: str):
    data = {
        'status': 'failed',
        'msg': error_msg,
    }
    response = jsonify(data)
    response.status_code = status_code
    return abort(response)
