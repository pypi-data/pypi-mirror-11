__author__ = 'zirony'


def success(data={}):
	if not isinstance(data, dict):
		raise ValueError('data must be the dict type')
	return {'status': 'success', 'data': data}


def fail(data={}):
	if not isinstance(data, dict):
		raise ValueError('data must be the dict type')
	return {'status': 'fail', 'data': data}


def error(message='', code=None, data=None):
	ret = {}
	if not isinstance(message, str):
		raise ValueError('message must be the str type')
	if code:
		if not isinstance(code, int):
			raise ValueError('code must be the int type')
		ret['code'] = code
	if data:
		if not isinstance(data, dict):
			raise ValueError('data must be the dict type')
		ret['data'] = data

	ret['status'] = 'error'
	ret['message'] = message
	return ret


def is_success(jsend_type):
	return jsend_type['status'] == 'success'


def is_fail(jsend_type):
	return jsend_type['status'] == 'fail'


def is_error(jsend_type):
	return jsend_type['status'] == 'error'
