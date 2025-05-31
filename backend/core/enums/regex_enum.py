from enum import Enum


class RegexEnum(Enum):
    NAME = (
        r'^[A-z][a-z]{,19}$',
        'Only alpha characters are allowed!',
    )
    SURNAME = (
        r'^[A-z][a-z]{,19}$',
        'Only alpha characters are allowed!',
    )
    STREET = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    CITY = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    REGION = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    COUNTRY = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    GENDER = (
        r'^[A-z][a-z]{,9}$',
        'Only alpha characters are allowed!',
    )
    CITY_LISTING = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    REGION_LISTING = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )
    COUNTRY_LISTING = (
        r'^[A-z][a-z]{,29}$',
        'Only alpha characters are allowed!',
    )

    def __init__(self, pattern:str, msg:str):
        self.pattern = pattern
        self.msg = msg