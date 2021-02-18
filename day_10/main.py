import typing


def get_device_jolt_rating(adapters: typing.List[int]) -> int:
    return max(adapters) + 3


def get_jolts_differences_after_connection(adapters: typing.List[int], device_jolt_rating: int) -> typing.Dict[int, int]:
    adapters.sort()

    jolts_steps = get_jolts_steps(adapters=adapters, device_jolt_rating=device_jolt_rating)
    jolts_differences = calculate_differences(jolts_steps=jolts_steps)

    return jolts_differences


def get_jolts_steps(adapters: typing.List[int], device_jolt_rating: int) -> typing.List[int]:
    jolts_steps = [0]
    last_jolt_rating = 0

    for adapter in adapters:
        if adapter == last_jolt_rating:
            continue

        if adapter > last_jolt_rating + 3:
            continue

        last_jolt_rating = adapter
        jolts_steps.append(last_jolt_rating)

    jolts_steps.append(device_jolt_rating)
    return jolts_steps


def chunk_jolts_steps(jolt_steps: typing.List[int]) -> typing.List[typing.List[int]]:
    chunks = []
    index = 0
    temp_jolt_steps = jolt_steps.copy()
    jolt_steps_len = len(temp_jolt_steps)

    while index <= jolt_steps_len - 1:

        if jolt_steps_len <= 2 or index == jolt_steps_len - 1:
            chunks.append(temp_jolt_steps)
            break

        if index == 0:
            index += 1
            continue

        previous_jolt = temp_jolt_steps[index - 1]
        current_jolt = temp_jolt_steps[index]

        if current_jolt - previous_jolt == 3:

            chunks.append(temp_jolt_steps[0:index])
            del temp_jolt_steps[0:index]
            index = 0
            jolt_steps_len = len(temp_jolt_steps)

        else:
            index += 1

    return chunks


def get_permutations_for_chunks(chunks: typing.List[typing.List[int]]) -> typing.List[int]:
    permutations = []

    for chunk in chunks:

        if len(chunk) < 3:
            permutations.append(1)
            continue

        permutations.append(len(get_permutation_for_chunk(chunk)))

    return permutations


def get_permutation_for_chunk(chunk: typing.List[int]) -> typing.List[typing.List[int]]:
    deleted_chunk_for_future_permutations: typing.List[typing.List[int]] = [chunk]

    index = 1
    end_index = len(chunk) - 2

    while index <= end_index:
        temp_chunk = chunk.copy()
        del temp_chunk[index]

        if can_delete_value_at_position(chunk, index) and \
                not is_permutation_already_found(deleted_chunk_for_future_permutations, temp_chunk):

            deleted_chunk_for_future_permutations.append(temp_chunk)
            nested_permutations = get_permutation_for_chunk(temp_chunk)

            for nested_permutation in nested_permutations:
                if not is_permutation_already_found(deleted_chunk_for_future_permutations, nested_permutation):
                    deleted_chunk_for_future_permutations.append(nested_permutation)

        index += 1

    return deleted_chunk_for_future_permutations


def can_delete_value_at_position(chunk: typing.List[int], index: int) -> bool:
    prev_value = chunk[index - 1]
    nex_val = chunk[index + 1]

    return nex_val - prev_value <= 3


def is_permutation_already_found(permutations: typing.List[typing.List[int]], permutation: typing.List[int]) -> bool:
    for p in permutations:
        if len(p) != len(permutation):
            continue

        are_the_same = False
        for index in range(len(p)):
            are_the_same = p[index] == permutation[index]

            if not are_the_same:
                break

        if are_the_same:
            return are_the_same

    return False


def calculate_permutations(permutations: typing.List[int]) -> int:
    multiplication = 1
    for p in permutations:
        multiplication *= p

    return multiplication


def calculate_differences(jolts_steps: typing.List[int]) -> typing.Dict[int, int]:
    differences = {}
    last_jolt_step = 0
    for i in range(len(jolts_steps)):
        if i == 0:
            continue

        difference = jolts_steps[i] - last_jolt_step
        last_jolt_step = jolts_steps[i]
        differences[difference] = differences.get(difference, 0) + 1

    return differences


def get_difference_multiplication(differences: typing.Dict[int, int], include_diff: typing.List[int]) -> int:
    result = 1

    for diff in include_diff:
        result *= differences.get(diff, 0)

    return result


def main(adapters: typing.List[str]):
    adapters = list(map(int, adapters))
    adapters.sort()

    device_jolt_rating = get_device_jolt_rating(adapters=adapters)

    # For getting the multiplication
    jolts_differences = get_jolts_differences_after_connection(adapters=adapters, device_jolt_rating=device_jolt_rating)
    multiplication_result = get_difference_multiplication(differences=jolts_differences, include_diff=[1, 3])
    print('Multiplication: {}'.format(multiplication_result))

    complete_jolt_steps = get_jolts_steps(adapters=adapters, device_jolt_rating=device_jolt_rating)
    chunk_jolts = chunk_jolts_steps(complete_jolt_steps)
    permutations_for_chunks = get_permutations_for_chunks(chunk_jolts)
    permutations = calculate_permutations(permutations_for_chunks)

    print('Number of permutations: {}'.format(permutations))

