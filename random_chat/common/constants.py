from enum import IntEnum
from typing import List, Tuple, Optional


class BaseIntEnum(IntEnum):
    @classmethod
    def get_choices(cls) -> List[Tuple]:
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_string_for_value(cls, value: int) -> Optional[str]:
        """
        This class method returns the string representation of an enum integer value if it exists in the enum.

        Eg:
        UserStatusType.get_string_for_type(1) returns UserStatusType.ONLINE
        UserGenderType.get_string_for_type(99) returns DO_NOT_WANT_TO_DISCOLSE

        """
        for item in cls:
            if item.value == value:
                return item.name
        return None

    @classmethod
    def get_obj_for_string(cls, type: str) -> "BaseIntEnum":
        """
        This method returns the enum object for the given string representation.

        Eg:
        UserStatusType.get_obj_for_string("ONLINE") returns UserStatusType.ONLINE
        UserGenderType.get_obj_for_string("MALE") returns UserGenderType.MALE

        Throws KeyError if the input string is invalid
        """
        return cls.__members__[type]


class UserStatusType(BaseIntEnum):
    ONLINE = 1
    OFFLINE = 2
    AVAILABLE = 3
    BUSY = 4


class UserGenderType(BaseIntEnum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

    DO_NOT_WANT_TO_DISCOLSE = 99
