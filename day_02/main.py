
def is_password_valid(password_dict):
    letter = password_dict.get('letter')
    password = password_dict.get('password')
    min_rep = password_dict.get('minRep')
    max_rep = password_dict.get('maxRep')
    repeats = int(password.count(letter))

    return min_rep <= repeats <= max_rep

def is_password_valid_new_version(password_dict):
    letter = password_dict.get('letter')
    password = password_dict.get('password')
    min_rep = password_dict.get('minRep')
    max_rep = password_dict.get('maxRep')
    repeats = int(password.count(letter))

    return (password[min_rep - 1] == letter and password[max_rep -1] != letter) \
           or (password[min_rep - 1] != letter and password[max_rep -1] == letter)


def get_password_dicts(password_metadata):
    password_dicts = []

    for password_meta in password_metadata:
        minMax = password_meta[0].split('-')
        letter = password_meta[1].split(':')
        given_password = password_meta[2].replace('\n', '')
        password = {
            "minRep": int(minMax[0]),
            "maxRep": int(minMax[1]),
            "letter": letter[0],
            "password": given_password
        }

        password_dicts.append(password)
    return password_dicts


with open('input.txt', 'r') as file:
    password_raw_metadata = file.readlines()

password_metadata = [(password_metadata.split(" ")) for password_metadata in password_raw_metadata]

password_dicts = get_password_dicts(password_metadata)
password_valid_state = [is_password_valid_new_version(password_dict) for password_dict in password_dicts]

print(password_valid_state.count(True))