from enum import Enum
import json
import re

class Debugger:
    debug = False
    write_log = False

    debug_file = None
    debug_file_path = 'debug.log'

    @staticmethod
    def log(message):
        if Debugger.debug:
            Debugger.log_message(message)
            print(message)

    @staticmethod
    def start_log():
        Debugger.write_log = True

        Debugger.debug_file = open(Debugger.debug_file_path, 'a')
        Debugger.log_message('\n\n START Debug \n\n')

    @staticmethod
    def stop_log():
        Debugger.log_message('\n END Debug \n\n')
        Debugger.write_log = False
        Debugger.debug_file.close()

    @staticmethod
    def log_message(message):
        if Debugger.write_log:
            Debugger.debug_file.write('{}\n'.format(message))


class RequireOption(Enum):
    REQUIRED = 1
    OPTIONAL = 2


valid_passport_template = dict(
    byr=RequireOption.REQUIRED,
    iyr=RequireOption.REQUIRED,
    eyr=RequireOption.REQUIRED,
    hgt=RequireOption.REQUIRED,
    hcl=RequireOption.REQUIRED,
    ecl=RequireOption.REQUIRED,
    pid=RequireOption.REQUIRED,
    cid=RequireOption.OPTIONAL,
)


class FieldValidator:
    def validate(self, field_name, field_value):

        validator = self._get_validator(field_name)
        return validator(field_value)

    def _get_validator(self, field_name):
        if field_name == 'byr':
            return self._valid_byr
        elif field_name == 'iyr':
            return self._valid_iyr
        elif field_name == 'eyr':
            return self._valid_eyr
        elif field_name == 'hgt':
            return self._valid_hgt
        elif field_name == 'hcl':
            return self._valid_hcl
        elif field_name == 'ecl':
            return self._valid_ecl
        elif field_name == 'pid':
            return self._valid_pid
        elif field_name == 'cid':
            return self._valid_cid
        else:
            raise ValueError('No field value validator: ', field_name)

    def _valid_byr(self, value: str) -> bool:
        Debugger.log('Asserting {} <= {} <= {} Result: {}'.format(1920, int(value), 2002, 1920 <= int(value) <= 2002))
        return len(value) == 4 and 1920 <= int(value) <= 2002

    def _valid_iyr(self, value: str) -> bool:
        Debugger.log('Asserting {} <= {} <= {} Result: {}'.format(2010, int(value), 2020, 2010 <= int(value) <= 2020))
        return len(value) == 4 and 2010 <= int(value) <= 2020

    def _valid_eyr(self, value: str) -> bool:
        Debugger.log('Asserting {} <= {} <= {} Result: {}'.format(2020, int(value), 2030, 2020 <= int(value) <= 2030))
        return len(value) == 4 and 2020 <= int(value) <= 2030

    def _valid_hgt(self, value: str) -> bool:
        metric_unit = ''
        metric_value = ''
        for char in value:
            if char.isalpha():
                metric_unit += char
            else:
                metric_value += char

        if metric_unit == 'cm':
            return self._valid_hgt_cm(metric_value)
        elif metric_unit == 'in':
            return self._valid_hgt_in(metric_value)
        else:
            return False

    def _valid_hgt_cm(self, value: str) -> bool:
        Debugger.log(
            'Asserting cm height {} <= {} <= {} Result: {}'.format(150, int(value), 193, 150 <= int(value) <= 193))
        return 150 <= int(value) <= 193

    def _valid_hgt_in(self, value: str) -> bool:
        Debugger.log(
            'Asserting in height {} <= {} <= {} Result: {}'.format(59, int(value), 76, 59 <= int(value) <= 76))
        return 59 <= int(value) <= 76

    def _valid_hcl(self, value: str) -> bool:
        pattern = re.compile('^#([0-9]|[a-f]){6}$')
        Debugger.log(
            'Asserting hair color {} match pattern: {}'.format(value, re.match(pattern, value) is not None))
        return re.match(pattern, value) is not None

    def _valid_ecl(self, value: str) -> bool:
        Debugger.log(
            'Asserting eye color {} is in color: {} match pattern: {}'.format(value, ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'], value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']))
        return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def _valid_pid(self, value: str) -> bool:
        Debugger.log(
            'Asserting pid {} match pattern: {}'.format(value, re.match('^[0-9]{9}$', value) is not None))
        return re.match('^[0-9]{9}$', value) is not None

    def _valid_cid(self, value: str) -> bool:
        Debugger.log('Cid ommited. Returned True')
        return True

class PassportValidator:
    valid_passport_temp = {}

    def __init__(self, valid_passport_dict):
        self.valid_passport_temp = valid_passport_dict
        self.field_validator = FieldValidator()

    def valid_passport(self, p):

        Debugger.log('Checking: {}'.format(p))

        for key in self.valid_passport_temp:
            Debugger.log('Key: {}, value: {}, is required: {}'.format(key, p.get(key, None), self.valid_passport_temp[key] != RequireOption.OPTIONAL))

            if p.get(key, None) is None and self.valid_passport_temp[key] != RequireOption.OPTIONAL:
                Debugger.log('Returned False because there is no field {} and it is required\n\n----------------\n\n'.format(key))
                return False

            elif not self.field_validator.validate(key, p.get(key, '')):
                Debugger.log('Returned False by field validator on field: {} for value: {}\n\n----------------\n\n'.format(key, p.get(key, '')))
                return False

        Debugger.log('Returned True\n\n----------\n\n')
        return True


class PassportExtractor:

    def extract_passports(self, data):
        data = data.split('\n\n')
        passport_raw_data = []

        for passport_raw_entry in data:
            raw_entry = passport_raw_entry\
                .replace('\n', ' ')\
                .split(' ')

            passport_raw_data.append(sorted(raw_entry))

        return map(self.create_passport_from_raw_data, passport_raw_data)

    def create_passport_from_raw_data(self, r_data):
        passport_obj = {}
        for d in r_data:
            key, value = d.split(':')
            passport_obj[key] = value
        return passport_obj


passport_extractor = PassportExtractor()
passport_validator = PassportValidator(valid_passport_template)

Debugger.start_log()

with open('input.txt') as file:

    raw_data = file.read()
    passports = passport_extractor.extract_passports(data=raw_data)

    valid_passports = 0

    open('positive_results.txt', 'w').close()
    open('negative_results.txt', 'w').close()
    negative_results_file = open('negative_results.txt', 'a')
    negative_results_file.write('RESULTS\n')

    positive_result_file = open('positive_results.txt', 'a')
    positive_result_file.write('RESULTS\n')

    for passport in passports:
        is_valid = passport_validator.valid_passport(passport)

        if is_valid:
            temp_p = {}

            for key in passport:
                if key != 'cid':
                    temp_p[key] = passport.get(key)
            valid_passports += 1
            positive_result_file.write(json.dumps(temp_p))
            positive_result_file.write('\n')
        else:
            negative_results_file.write(json.dumps(passport))
            negative_results_file.write('\n')

    positive_result_file.close()
    print(valid_passports)

Debugger.stop_log()