#!/usr/bin/env python3
"""First Task"""


import re
from typing import List
import logging

PII_FIELDS = ('name', 'email',
              'phone',
              'ssn', 'password'
              #   'ip',
              # 'last_login', 'user_agent'
              )


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


def get_logger() -> logging.Logger:
    """function that returns a logging object"""
    name = "user_data"
    level = logging.INFO
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())
    logger.handlers[0].setFormatter(formatter)
    return logger


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
