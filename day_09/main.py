import typing


def find_weak_number(numbers: typing.List[int], preamble_size: int) -> int:
    index = preamble_size

    while index < len(numbers):
        number, is_weak = is_weak_number(numbers=numbers, preamble_size=preamble_size, index=index)
        index += 1

        if is_weak:
            return number


def is_weak_number(numbers: typing.List[int], preamble_size: int, index: int) -> (int, bool):
    preamble, number = get_preamble_and_number(numbers=numbers, index=index, preamble_size=preamble_size)
    is_weak = not is_number_valid(preamble=preamble, number=number)

    return number, is_weak


def get_preamble_and_number(numbers: typing.List[int], index: int, preamble_size: int) -> (typing.List[int], int):
    return numbers[index - preamble_size:index], numbers[index]


def is_number_valid(preamble, number) -> bool:
    sums = get_preamble_sums(preamble=preamble)

    return number in sums


def get_preamble_sums(preamble: typing.List[int]) -> typing.List[int]:
    sums: typing.List[int] = []

    for a_index in range(len(preamble)):
        for b in range(len(preamble) - a_index - 1):
            b_index = b + a_index + 1
            sums.append(preamble[a_index] + preamble[b_index])

    return sums


def find_contiguous_set(numbers: typing.List[int], number: int) -> typing.List[int]:
    # print('Input for second part: numbers: {}, number: {}'.format(numbers, number))
    index = 0
    numbers_to_sum: typing.List[int] = None

    while index < len(numbers) - 2 and numbers_to_sum is None:
        numbers_to_sum = find_number_to_sum(numbers, number, index)
        index += 1

    return numbers_to_sum


def find_number_to_sum(numbers: typing.List[int], number: int, index: int) -> typing.List[int]:
    numbers_to_sum: typing.List[int] = [numbers[index]]
    total_sum: int = 0

    index += 1

    while total_sum < number and index < len(numbers):
        numbers_to_sum.append(numbers[index])
        total_sum = sum(numbers_to_sum)
        index += 1

    # print('Number {}, Numbers to sum: {}, sum: {}, assertion: {}'.format(number, numbers_to_sum, sum(numbers_to_sum), number == sum(numbers_to_sum)))
    return numbers_to_sum if total_sum == number else None


def main(input_list: typing.List[str]):
    numbers = list(map(int, input_list))

    weak_number = find_weak_number(numbers=numbers, preamble_size=25)
    contiguous_set = find_contiguous_set(numbers=numbers, number=weak_number)

    min_value, max_value = min(contiguous_set), max(contiguous_set)
    print(min_value + max_value)
