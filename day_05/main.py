def get_seat_metadata(code):
    seat_row_code = code[:7]
    seat_column_code = code[7:].replace('\n', '')
    return {'seat_column_code': seat_column_code, 'seat_row_code': seat_row_code}


def decode_position_code(seat_metadata):
    row_code = seat_metadata.get('seat_row_code')
    column_code = seat_metadata.get('seat_column_code')

    row = get_int_from_code(row_code, ('B', 'F'))
    collum = get_int_from_code(column_code, ('R', 'L'))

    return {'seat_row': row, 'seat_column': collum}


def get_int_from_code(code, one_zero_tuple):
    bits = get_bits_from_code(code, one_zero_tuple)
    return bits_to_int(bits)


def get_bits_from_code(code, one_zero_tuple):
    one, zero = one_zero_tuple
    bits = ''

    for char in code:
        bits += '0' if char == zero else '1'

    return bits


def bits_to_int(bits: list) -> int:
    return int(bits, 2)


def calculate_seat_id(seat_poisition):
    row = seat_poisition.get('seat_row')
    column = seat_poisition.get('seat_column')

    return row * 8 + column


with open('input.txt') as file:
    codes = file.readlines()

    seats_metadata = map(get_seat_metadata, codes)
    seats_positions = map(decode_position_code, seats_metadata)
    seats_ids = list(map(calculate_seat_id, seats_positions))
    seats_ids.sort()

    for i in range(len(seats_ids) - 1):
        if i == 0 or i == len(seats_ids):
            continue

        if seats_ids[i -1] - seats_ids[i] != -1:
            print('Lack of next seat', seats_ids[i] - 1)

