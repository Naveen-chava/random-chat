from enum import IntEnum
from typing import List, Tuple, Optional


class BaseIntEnum(IntEnum):
    @classmethod
    def get_choices(cls) -> List[Tuple]:
        return [(item.value, item.name) for item in cls]

    @classmethod
    def get_string_for_type(cls, value: int) -> Optional[str]:
        for item in cls:
            if item.value == value:
                return item.name
        return None


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
