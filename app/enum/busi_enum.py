from enum import Enum


class BusiEnum(Enum):
    """
    业务枚举
    """
    VISIBILITY_PUBLIC = (u'public', u'公开')
    VISIBILITY_PRIVATE = (u'private', u'私有')

    USER_STATE_ACTIVE = (u'active', u'可用')
    USER_STATE_BLOCK = (u'blocked', u'禁用')

    @staticmethod
    def get_key(element):
        return element.value[0]

    @staticmethod
    def get_desc(element):
        return element.value[1]