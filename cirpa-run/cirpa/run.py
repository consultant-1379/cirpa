#!/usr/bin/env python

import sys
import argparse
import json
import os
import importlib

from cirpa.startbase import StartBase
from cirpa.hasharguments import HashArguments

'''
The Start class creates the argument tree that holds all the registered classes from the supplied config file

The option --config gives you the flexibility to override the default config/cirpa.conf path

For an example setup with a config file and start classes check the examples folder and the start.sh script

'''


class Start:

    filename = "config/cirpa.conf"

    # this function handles the loading of an module from a file
    def load_module(self, filename):
        sys.path.append(os.path.dirname(filename))
        mname = os.path.splitext(os.path.basename(filename))[0]
        imported = importlib.import_module(mname)
        sys.path.pop()
        return imported

    # constructor
    # argv needs to be in the same format as sys.argv
    def __init__(self, argv):

        self.arguments = HashArguments()

        # handle the default argument --config first before doing anything else
        parentParser = argparse.ArgumentParser("CIRPA arguments", conflict_handler="resolve", add_help=False)
        parentParser.add_argument('--config', dest='config', required=False, default=None)
        args, notParsedArgs = parentParser.parse_known_args(argv)

        # override default filename
        if args.config:
            self.filename = args.config

        # load the JSON config
        if os.path.isfile(self.filename):
            with open(self.filename, "r+") as f:
                try:
                    self.modules = json.loads(f.read())
                except:
                    print("Error, loading config file: %s" % self.filename)
                    sys.exit(1)
        else:
            print("Error, config file: %s does not exist" % self.filename)
            sys.exit(1)

        # import all modules and instantiate their start classes
        try:

            for k, c in self.modules.items():
                if os.path.isfile(k):
                    m = self.load_module(k)
                else:
                    # load as regular module
                    m = importlib.import_module(k)

                classObject = (getattr(m, c)())

                # all start classes needs to inherit from StartBase
                if not isinstance(classObject, StartBase):
                    raise TypeError("class %s does not inherit StartBase" % c)

                self.arguments.add_arguments(classObject.get_path(), classObject)

        except ImportError as err:
            print('Error with %s(%s): %s' % (k, c, err))
            sys.exit(1)

        # creating the parser object used by all the start classes
        parser = argparse.ArgumentParser(conflict_handler="resolve", parents=[parentParser])
        self.parser = parser

        # adding arguments from the start classes
        for key, obj in self.arguments.items():
            obj.arguments(self.parser)

        # parse the remaining arguments, skipping the first item which is the command line name
        self.args = self.parser.parse_args(notParsedArgs[1:])

    # the execute function have a dependecy that self.args exists
    def execute(self):

        # find the correct start class object from the argument combination
        try:
            obj = self.arguments.get_argument_object(vars(self.args))
            return obj.execute(vars(self.args))

        except Exception as e:
            # we are not expected to get here unless an start class is behaving bad
            print(e)
            sys.exit(1)

        print("Error, no start class found with arguments: %s" % (vars(self.args)))
        sys.exit(1)


def main():
    starts = Start(sys.argv)
    return starts.execute()
