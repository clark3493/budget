import pathmagic
import csv
import logging
from datetime import datetime
from parser_statement import Parser


class BofAParser(Parser):

    START_LINE = 'Date,Description,Amount,Running Bal.'

    def __init__(self, filepath):
        super(BofAParser, self).__init__(filepath)
        self.transactions = []

        self.logger = logging.getLogger(__name__)

    def parse_statement(self):
        start = False
        with open(self.filepath) as csvfile:
            self.reader = csv.reader(csvfile)
            for row in self.reader:
                if start:
                    data = self.read_transaction(row)
                    if data is not None:
                        self.transactions.append(data)
                if ",".join(row) == self.START_LINE:
                    start = True

        return self.transactions

    def read_transaction(self, line):
        """
        Takes a parsed csv line from a BofA statement and returns the
        corresponding transaction date, description, value and running
        balance
        :param line: parsed csv transaction line from a BofA statement
        :type line: list(str)
        :return: (date, description, value, running balance)
        :rtype: tuple(date, str, float, float)
        """
        try:
            if line[0]:
                transaction_date = datetime.strptime(line[0], '%m/%d/%Y').date()
            else:
                transaction_date = None

            description = line[1]

            if line[2]:
                value = round(float(line[2]), 2)
            else:
                value = None

            if line[3]:
                running_balance = round(float(line[3]), 2)
            else:
                running_balance = None

            return (transaction_date,
                    description,
                    value,
                    running_balance)

        except Exception as e:
            # ADD BETTER ERROR HANDLING
            self.logger.error(e)
            self.logger.debug("line = " + str(line))
            return None



