import argparse
import importlib
import utils
import typing
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--day', help="Task day", type=str, required=True)
parser.add_argument('-f', '--file', help="File of input from task", type=str)


def run_test_script(day: int, file: str):
    target_script_directory = 'day_{}'.format(day)
    logging.basicConfig(filename='{}/debug.txt'.format(target_script_directory), level=logging.DEBUG, filemode='w')

    file_input = load_file_input('{}/{}'.format(target_script_directory, file))

    mod = importlib.import_module('day_{}.main'.format(day))
    mod.main(file_input)


def load_file_input(filename: str) -> typing.List[str]:
    with open(filename) as file:
        return list(map(utils.remove_next_line_signs, file.readlines()))


if __name__ == '__main__':
    args = parser.parse_args()
    day = args.day.zfill(2)
    file = args.file or 'input.txt'
    run_test_script(day=day, file=file)
