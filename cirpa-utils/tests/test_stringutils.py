import pytest
from cirpa.utils.stringutils import StringUtils, ValueNotInBoolList

"""Test of the string utility function str2bool"""


def test_str2bool_valid_bool():
    s = StringUtils()
    valid_bool = ('yes', 'true', 't', 'y', '1', 'YES', 'TRUE', 'T', 'Y', 'no', 'false', 'f', 'n', '0', 'NO', 'FALSE', 'F', 'n')
    for value in valid_bool:
        s.str2bool(value)


def test_str2bool_invalid_value():
    s = StringUtils()
    with pytest.raises(ValueNotInBoolList) as excinfo:
        s.str2bool('5')
    assert str(excinfo.value) == ("Invalid value: " + str('5'))
