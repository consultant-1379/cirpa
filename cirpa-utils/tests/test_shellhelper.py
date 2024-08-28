from subprocess import CalledProcessError
import pytest
from cirpa.utils.shellhelper import call, execute

'''Test of the shellhelper functions, call and execute.'''


def test_call_success_debug_false():
    assert call(["ls", "-l"], debug=False) == 0


def test_call_success_no_debug_option():
    assert call(["ls", "-l"]) == 0


def test_call_success_debug_true():
    assert call(["ls", "-l"], debug=True) == 0


def test_call_failing_returncode_1():
    assert call(["false"], debug=True) == 1


def test_call_failing_with_none_existing_command():
    with pytest.raises(OSError):
        call(["blabla"])


def test_execute_success():
    assert execute(["echo", "Hello Hakan"]) == b"Hello Hakan\n"


def test_execute_succes_debug_false():
    assert execute(["echo", "Hello Hakan"], debug=False) == b"Hello Hakan\n"


def test_execute_failing_with_none_existing_command():
    with pytest.raises(OSError):
        execute(["blabla"])


def test_execute_failing_with_faulty_ls_option():
    with pytest.raises(CalledProcessError):
        execute(["ls", "-j"])
