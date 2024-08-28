import hashlib
import collections


class Optional(str):
    pass


class RegExp(str):
    hashValue = 80085
    pass


class HashArguments():

    def __init__(self):
        self.arguments = collections.OrderedDict()

    def items(self):
        return self.arguments.items()

    def add_arguments(self, arguments, obj):
        self.arguments[self._hash_args_md5(arguments)] = obj

    def get_argument_object(self, arguments):
        return self.arguments[self._hash_args_md5(arguments)]

    def _hash_args_md5(self, arguments):
        hashValue = ""
        for key in sorted(arguments):
            value = arguments[key]

            if type(value) is Optional:
                continue

            # This continue is executed but CPython's peephole optimizer replaces
            # a jump to a continue with a jump to the top of the loop and
            # the coverage measurement treats it as uncovered
            if value is None:
                continue  # pragma: no cover

            # append value hash
            if type(value) is RegExp:
                hashValue += str(RegExp.hashValue)
            else:
                # this takes cares of all built in types
                m = hashlib.md5()
                m.update(str(value).encode('utf-8'))
                hashValue += m.hexdigest()

            # append key to hash
            hashValue += str(key)

        # calculate the md5 hash for the arguments
        m = hashlib.md5()
        m.update(hashValue.encode('utf-8'))
        retval = m.hexdigest()

        return retval
