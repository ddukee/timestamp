#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from argparse import ArgumentParser
from argparse import Action
import sys
import re


class DatetimeParseAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            date = None
            if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}$', values):
                # YYYY-MM-DD HH:MM:SS.mmmmmm
                ft = '%Y-%m-%d %H:%M:%S.%f'
                date = datetime.strptime(values.strip("'"), ft)
            elif re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', values):
                # YYYY-MM-DD HH:MM:SS
                ft = '%Y-%m-%d %H:%M:%S'
                date = datetime.strptime(values.strip("'"), ft)
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', values):
                # YYYY-MM-DD
                ft = '%Y-%m-%d'
                date = datetime.strptime(values.strip("'"), ft)
            if date:
                setattr(namespace, self.dest, date)


class TimestampParseAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            setattr(namespace, self.dest, datetime.fromtimestamp(float(values)))


def main():
    parser = ArgumentParser(prog='timestamp',
                            description='''
                            convert formatted datetime to unix timestamp or
                            convert unix timestamp to formatted datetime''')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t',
                       action=TimestampParseAction,
                       metavar='timestamp',
                       dest='timestamp',
                       help='unix timestamp')
    group.add_argument('-d',
                       action=DatetimeParseAction,
                       metavar='datetime',
                       dest='datetime',
                       help='formatted date')

    namespace = parser.parse_args(sys.argv[1:])

    if namespace.datetime:
        print(int(namespace.datetime.timestamp()))
    elif namespace.timestamp:
        print(namespace.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        # no options a specify, print current timestamp
        print(int(datetime.today().timestamp()))


if __name__ == '__main__':
    main()
