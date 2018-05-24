import pathmagic
import argparse
import logging
import shlex
import sys

from database import Database


class DatabaseCLI(Database):

    VERSION = 1.0

    def __init__(self, configuration):
        super(DatabaseCLI, self).__init__(configuration)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=configuration.LOGLEVEL)

        self.parser = argparse.ArgumentParser(description='Command line interface for a database')

    def define_args(self):
        self.define_basic_args()

    def define_basic_args(self):
        self.parser.add_argument('-q', '--quit', action='store_true',
                                 dest='quit',
                                 help='Exit the command line interface')
        self.parser.add_argument('-s', '--sql', type=str, nargs='*',
                                 dest='CMD', metavar='SQL_CMD',
                                 help='Execute one or more SQL statements')
        self.parser.add_argument('-v', '--version', action='version',
                                 version='DatabaseCLI v' + str(self.VERSION))

    def evaluate_args(self, args):
        self.evaluate_basic_args(args)

    def evaluate_basic_args(self, args):
        if args.quit is True:
            self.quit()

        if args.CMD:
            for cmd in args.CMD:
                self.sql_cmd(cmd)

    @staticmethod
    def get_command():
        return input('>>>')

    def main(self):
        self.define_args()
        print(self.main_msg())
        while True:
            args = None
            try:
                args = self.parser.parse_args(shlex.split(self.get_command()))
                self.evaluate_args(args)
                continue

            except SystemExit:
                if args:
                    if args.quit is True:
                        self.quit()
                else:
                    continue

            except Exception as e:
                print("An error occurred:\n{}".format(e))
                print("Use -q or --quit to exit the command line interface")
                continue

    @staticmethod
    def main_msg():
        msg = "DATABASE COMMAND LINE INTERFACE\nEnter -h or --help for command help"
        return msg

    @staticmethod
    def quit():
        sys.exit(0)
