from enum import Enum


class ResponseEnum(Enum):
    """
    返回response中的json code码
    """
    SUCCESS = (1000, u'成功')

    INVALID_TOKEN = (9001, u'无效的token')
    INVALID_TOKEN_EXP = (9002, u'token过期')
    INVALID_TOKEN_ERR = (9003, u'token信息不完整')
    INVALID_TICKET = (9004, u'无效的ticket')
    INVALID_PARAMS = (9000, u'无效的参数')

    MISSING_USERNAME_OR_PASSWORD = (9001, u'登录用户名或密码不能为空')
    LOGIN_FAILED = (9001, u'账户不存在或账号密码错误')

    PROJECT_NAME_CANNOT_BE_EMPTY = (9005, u'仓库名称不能为空')
    PROJECT_PATH_NOT_VALID = (9006, u'仓库路径不符合要求，必须由字母，数字，短横线和下划线组成')
    NAME_OR_PATH_ALREADY_EXISTS = (9007, u'name或path已经存在')
    VISIBILITY_NOT_VALID = (9008, u'visibility只允许填写private和public')

    ACCOUNT_INFO_CANNOT_BE_EMPTY = (9010, u'用户名，邮箱或姓名不能为空')
    PASSWORD_CANNOT_BE_EMPTY = (9011, u'密码不能为空')
    ACCOUNT_CONFLICT = (9012, u'该用户名已被注册')
    EMAIL_CONFLICT = (9013, u'该邮箱已被注册')
    USER_ID_CANNOT_BE_EMPTY = (9014, u'user_id不能为空')
    OLDPASSWORD_IS_NOT_MATCH = (9015, u'原密码不正确')
    USERNAME_INVALID = (9016, u'用户名无效，必须是小写字母和数字并且以字母开头')
    EMAIL_INVALID = (9017, u'邮箱地址无效')

    OBJECT_NOT_FOUNT = (9009, u'目标对象不存在')

    SERVER_ERROR = (9500, u'服务器出错')
    PERMISSION_ERROR = (9401, u'无权限')

    UNKNOW_ERROR = (9999, u'未知错误')

    @staticmethod
    def get_code(element):
        return element.value[0]

    @staticmethod
    def get_msg(element):
        return element.value[1]
