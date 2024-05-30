#!/usr/bin/env python3
"""First Task"""


import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """function that returns the log message obfuscated"""
    for field in fields:
        # must be non greedy, to stop at first separator
        regex = r"{}=.*?{}".format(field, separator)
        message = re.sub(regex,
                         f"{field}={redaction}{separator}",
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        redacted = filter_datum(self.fields, "***", record.getMessage(), ";")
        record.message = redacted
        record.asctime = self.formatTime(record, self.datefmt)
        return self.formatMessage(record)
        # NotImplementedError
