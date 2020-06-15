class SvnOperateException(Exception):
    def __init__(self, status, output):
        self.status = status
        self.output = output

    def get_status(self):
        return self.status

    def get_output(self):
        return self.output
