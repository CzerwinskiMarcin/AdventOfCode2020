def prepare_answers_data(raw_answers_input: str):
    groups_answers = get_group_answers(raw_answers_input)
    return list(map(get_persons_answers, groups_answers))


def get_group_answers(raw_answers_input: str) -> list:
    return raw_answers_input.split('\n\n')


def get_persons_answers(group_answers: str) -> list:
    return group_answers.split('\n')


def get_all_answers_for_group(group_answers: list) -> list:
    answers = []
    for person_answers in group_answers:
        for answer in person_answers:
            answers.append(answer)

    return answers


def remove_duplicates_from_answers(group_answers: list) -> list:
    return list(set(group_answers))


def keep_only_common_answers(group_answers: list) -> list:
    persons_number = len(group_answers)
    all_answers = get_all_answers_for_group(group_answers)
    unique_answers = remove_duplicates_from_answers(all_answers)

    repeated_answers = []
    for answer in unique_answers:
        if all_answers.count(answer) == persons_number:
            repeated_answers.append(answer)

    return repeated_answers


def count_answers(all_answers: list) -> int:
    answers_sum = 0

    for group_answers in all_answers:
        answers_sum += len(group_answers)

    return answers_sum


with open('input.txt') as file:
    raw_data = file.read()
    answers = prepare_answers_data(raw_data)
    repeated_answers = list(map(keep_only_common_answers, answers))
    print(count_answers(repeated_answers))
