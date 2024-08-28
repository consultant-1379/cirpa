import sys
import traceback
import subprocess
import shlex


# returns stdout/stderr instead of the return value of the command
def execute(command, debug=True):
    if debug:
        for cmd in command:
            sys.stdout.write(cmd + " ")
        sys.stdout.flush()
        print("")
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT)
    except:
        if debug:
            traceback.print_exc(file=sys.stdout)
        raise


def call(command, debug=False):

    if debug:
        for cmd in command:
            sys.stdout.write(cmd + " ")
        sys.stdout.flush()
        print("")
    returnValue = subprocess.call(command, stderr=subprocess.STDOUT)
    return returnValue


def call_as_user(user, command, debug=False):
    '''Executes command with specified user'''

    _command = 'su ' + user + ' -c "' + ' '.join(command) + '"'
    retcode = 1
    if debug:
        sys.stdout.write(_command)
        sys.stdout.flush()
        print("")
    try:
        retcode = subprocess.call(shlex.split(_command))
        if retcode != 0:
            print("Execution failed: ", retcode)
        return retcode
    except Exception as e:
        print("Execution failed: ", e)
        return retcode