class ValueNotInBoolList(Exception):
    """Raises ValueNotInBoolList when input is invalid in str2bool function."""
    pass


class StringUtils:

    """This utility class is for string operations"""

    def str2bool(self, value):
        """This function converts string values from the argument to boolean."""
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif value.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise ValueNotInBoolList("Invalid value: " + (value))
