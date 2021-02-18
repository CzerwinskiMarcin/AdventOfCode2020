import re
import typing


def trim(string: str) -> str:
    return string.lstrip().rstrip()


def str_to_int(string_number: str) -> int:
    try:
        return int(string_number)
    except ValueError:
        print('Cannot convert {} to number!'.format(string_number))


def find_digit(string: str) -> int:
    return list(map(str_to_int, re.findall(r'\d+', string)))[0]


def get_file_lines(file: str) -> typing.List[str]:
    with open(file) as file:
        return file.readlines()


def remove_next_line_signs(line: str) -> str:
    return line.replace('\n', '')