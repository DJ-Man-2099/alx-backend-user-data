#!/usr/bin/env python3
"""First Task"""


import os
import re
from typing import List
import logging
from mysql.connector import connect

PII_FIELDS = ('name', 'email',
              'phone',
              'ssn', 'password')


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
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # print(logger)
    return logger


def get_db() -> object:
    """function that returns a database connection object"""
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.environ.get('PERSONAL_DATA_DB_NAME', 'my_db')
    connection = connect(
        user=user,
        password=password,
        host=host,
        database=db
    )
    return connection
    # return None


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
