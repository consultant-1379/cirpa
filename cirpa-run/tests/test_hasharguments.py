import pytest

from cirpa.hasharguments import HashArguments, Optional, RegExp


def test_with_regexp():
    hashArgs = HashArguments()
    path = {"arg1": "nisse", "regexp": RegExp(".+"), "arg2": "olle"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(path)


def test_with_bool():
    hashArgs = HashArguments()
    path = {"arg1": "nisse", "boolean": True, "arg2": "olle"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(path)


def test_with_optional():
    hashArgs = HashArguments()
    path = {"arg1": "1", "optional": Optional("abc"), "arg2": "2"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(path)


def test_with_several_optional():
    hashArgs = HashArguments()
    path = {"arg1": "1", "optional": Optional("abc"), "optional1": Optional("def"), "arg2": "2"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(path)


def test_without_optional_input():
    hashArgs = HashArguments()
    path = {"arg1": "1", "optional": Optional("abc"), "arg2": "2"}
    args = {"arg1": "1", "arg2": "2"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(args)


def test_without_optional_added_but_as_input():
    hashArgs = HashArguments()
    path = {"arg1": "1", "arg2": "2"}
    args = {"arg1": "1", "optional": Optional("abc"), "arg2": "2"}

    hashArgs.add_arguments(path, "data")
    assert "data" == hashArgs.get_argument_object(args)


def test_key_error():
    hashArgs = HashArguments()
    path = {"arg1": "1", "optional": Optional("abc"), "arg2": "2"}
    args = {"arg1": "2", "arg2": "1"}

    hashArgs.add_arguments(path, "data")
    with pytest.raises(KeyError):
        hashArgs.get_argument_object(args)


def test_itererate_over_arguments():
    hashArgs = HashArguments()

    data = "hello world! "
    b1 = [({"os": "sles12", "compiler": "rcs-arm", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-i686", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-ppc", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-x64", "repo": "com-main"}, data)]
    b1 += [({"os": "rhel6", "compiler": "native", "repo": "com"}, data)]
    b1 += [({"os": "rhel6", "compiler": "native", "repo": "com-main"}, data)]
    b1 += [({"os": "sles11", "compiler": "lsb", "repo": "com-main"}, data)]
    b1 += [({"os": "sles11", "compiler": "native", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "native", "repo": "com"}, data)]
    b1 += [({"os": "sles12", "compiler": "cpp11", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "native", "repo": "com-main"}, data)]

    i = 0
    for b in b1:
        i += 1
        hashArgs.add_arguments(b[0], b[1] + str(i))

    i = 0
    for key, value in hashArgs.items():
        i += 1
        assert value == data + str(i)


def test_big_argument_list():
    hashArgs = HashArguments()

    data = "hello world! "
    b1 = [({"os": "sles12", "compiler": "rcs-arm", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-i686", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-ppc", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "rcs-x64", "repo": "com-main"}, data)]
    b1 += [({"os": "rhel6", "compiler": "native", "repo": "com"}, data)]
    b1 += [({"os": "rhel6", "compiler": "native", "repo": "com-main"}, data)]
    b1 += [({"os": "sles11", "compiler": "lsb", "repo": "com-main"}, data)]
    b1 += [({"os": "sles11", "compiler": "native", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "native", "repo": "com"}, data)]
    b1 += [({"os": "sles12", "compiler": "cpp11", "repo": "com-main"}, data)]
    b1 += [({"os": "sles12", "compiler": "native", "repo": "com-main"}, data)]

    i = 0
    for b in b1:
        i += 1
        hashArgs.add_arguments(b[0], b[1] + str(i))

    i = 0
    for b in b1:
        i += 1
        obj = hashArgs.get_argument_object(b[0])
        assert obj == data + str(i)
