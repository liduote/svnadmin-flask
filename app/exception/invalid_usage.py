from app.enum import ResponseEnum


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, status_code=None, payload=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        if not payload:
            self.payload = ResponseEnum.UNKNOW_ERROR
        self.payload = payload

    def to_dict(self):
        rv = dict()
        if type(self.payload) == ResponseEnum:
            rv['code'] = ResponseEnum.get_code(self.payload)
            rv['message'] = ResponseEnum.get_msg(self.payload)
        elif type(self.payload) == tuple:
            rv['code'] = self.payload[0]
            rv['message'] = self.payload[1]
        else:
            rv['message'] = self.payload
        return rv



