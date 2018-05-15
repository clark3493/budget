import logging

class Parser(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.reader = None

        self.logger = logging.getLogger(__name__)
