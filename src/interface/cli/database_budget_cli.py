import pathmagic
import argparse
import logging

from database_budget import BudgetDatabase
from src.interface.cli.database_cli import DatabaseCLI

class BudgetDatabaseCLI(BudgetDatabase, DatabaseCLI):

    def __init__(self, configuration):
        super(BudgetDatabaseCLI, self).__init__(configuration)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=configuration.LOGLEVEL)

        self.parser = argparse.ArgumentParser(description='Command line interface for a budget database')

    def define_args(self):
        self.define_basic_args()

    def evaluate_args(self):
        self.evaluate_basic_args()

    @staticmethod
    def main_msg():
        msg = "DATABASE COMMAND LINE INTERFACE\nEnter -h or --help for command help"
        return msg








