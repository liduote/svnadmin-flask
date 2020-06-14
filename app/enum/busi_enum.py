from enum import Enum


class BusiEnum(Enum):
    """
    业务枚举
    """
    VISIBILITY_PUBLIC = (u'public', u'公开')
    VISIBILITY_PRIVATE = (u'private', u'私有')

    @staticmethod
    def get_key(element):
        return element.value[0]

    @staticmethod
    def get_desc(element):
        return element.value[1]