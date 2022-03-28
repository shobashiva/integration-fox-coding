import csv
import os
import pathlib
import random
import string
import sys

import argparse
from datetime import datetime

ROWS_DEFAULT = 50


class MyVerboseParser(argparse.ArgumentParser): 
    ''' modify argparse to display full usage text '''
    def error(self, message):
        sys.stderr.write(f'ERROR: {message}\n')
        self.print_help()
        sys.exit(2)


def column_data(s):
    try:
        column_name, column_type = [x.strip() for x in s.split(',')]
        if (
            set(column_name).difference(string.ascii_letters + string.digits)
            or len(column_name) == 0
        ):
            raise TypeError(
                'Column name must be a non empty string '
                'without special characters'
            )
        if column_type in ['integer', 'string']:  # check for correct types
            return column_name, column_type
        else:
            raise TypeError(
                'Column type must be "integer" or "string"'
            )
    except (ValueError):
        raise TypeError(
            'Form of column argument must be: column_name,type'
        )


def save_path(s):
    '''
        The expected behavior around the output directory was unclear from the
        instructions, I'll make a decision here that if the directories
        don't exist, we'll assume the user either has the ability to create
        those directories (and allow write permissions), or that they shouldn't
        be writing files there
    '''
    if os.path.exists(pathlib.Path(s).absolute()):
        return s

    parent = pathlib.Path().resolve()

    if os.path.exists(os.path.join(parent, s)):
        return os.path.join(parent, s)
    else:
        raise ValueError(
            'New directories will not be created, '
            'output path must already exist and write permissions '
            'must be enabled'
        )


def parse_arguments():
    parser = MyVerboseParser(
        description=(
            'A script, that when executed from the command line can accept up '
            'to three '
            'named options and output a csv file in a local directory of the '
            'server we execute it from'
        ),
        formatter_class=argparse.MetavarTypeHelpFormatter
    )
    parser.add_argument('--rows', default=ROWS_DEFAULT, type=int, help=(
                f'will dictate the number of rows in the output '
                f'csv file (default: {ROWS_DEFAULT})'
        )
    )
    parser.add_argument(
        '--output_path',
        type=save_path,  # custom path checker
        default=pathlib.Path().resolve(),
        help=(
            f'where the generated csv file will be saved '
            f'new directories will not be created and write '
            f'permissions must already be in place '
            f'(default: current directory)'
        ))
    parser.add_argument('--column', nargs='+', type=column_data, help=(
                f'form of the argument must be: column_name,type where '
                f'type is either "integer" or "string" - '
                f'MUST be specified at least once but can be specified '
                f'multiple times'
        ),
        required=True
    )
    args = parser.parse_args()
    return args


def get_now():  # for ease of testing filename
    return datetime.now()


def get_filename():
    return f'{get_now().strftime("%Y-%m-%d-%H_%M_%S")}.csv'


def get_random_string():
    return ''.join(random.choices(
        string.ascii_letters,
        k=random.choices(range(1, 10), k=1)[0]  # random length less than 10
      )
    )


def get_value(column_type):
    if column_type == 'string':
        return get_random_string()

    return random.randint(0, 10000)


def get_column_types(args):
    return [x[1] for x in args.column]


def get_headers(args):
    return [x[0] for x in args.column]


def generate_csv(column_types, rows):
    return [[get_value(t) for t in column_types] for i in range(rows)]


def main(args):
    headers = get_headers(args)
    column_types = get_column_types(args)
    rows = args.rows
    write_path = os.path.join(
            args.output_path,
            get_filename()
    )

    csv_rows = generate_csv(column_types, rows)
    with open(write_path, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(csv_rows)


if __name__ == '__main__':
    args = parse_arguments()
    sys.exit(main(args))
