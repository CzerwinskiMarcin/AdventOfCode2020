from enum import Enum
import typing


class BootState(Enum):
    Start = 0,
    Running = 1,
    Terminate = 2,
    Infinity = 3

class Command(Enum):
    nop = 0,
    acc = 1,
    jmp = 2


def get_command(command: str) -> Command:
    if command == 'nop':
        return Command.nop
    elif command == 'acc':
        return Command.acc
    elif command == 'jmp':
        return Command.jmp
    else:
        raise ValueError(command)


class Step:
    previous_index: int = None
    next_index: int = None
    index: int
    command: Command
    command_value: int

    def __init__(self, index: int, command: Command, command_value: int):
        self.index = index
        self.command = command
        self.command_value = command_value

    def update_previous_index(self, previous_index: int):
        self.previous_index = previous_index or self.previous_index

    def update_next_index(self, next_index):
        self.next_index = next_index or self.next_index

    def already_executed(self) -> bool:
        return self.next_index is not None

    def __str__(self):
        return '{} {}'.format(self.command, self.command_value)

    def __repr__(self):
        return self.__str__()


class StepConveter:

    def convert_step(self, index: int, step: str) -> Step:
        command_str, value = step.split()

        return Step(index=index, command=get_command(command_str), command_value=int(value))

    def convert_steps(self, steps: typing.List[str]) -> typing.List[Step]:
        converted_steps: typing.List[Step] = []
        for i in range(len(steps)):
            step = self.convert_step(i, steps[i])
            converted_steps.append(step)

        return converted_steps

    def link_steps(self, steps: typing.List[Step]) -> (int, BootState):
        index = 0
        step_count = 0
        acc = 0
        boot_state = BootState.Running

        while step_count <= len(steps) and boot_state not in [BootState.Infinity, BootState.Terminate]:
            step = steps[index]

            (next_index, acc_value) = StepExecutor.execute_step(step, acc)

            acc = acc_value
            index = next_index
            step_count += 1

            if next_index >= len(steps):
                boot_state = BootState.Terminate
                continue

            next_step = steps[next_index]

            if next_step.already_executed():
                boot_state = BootState.Infinity
                continue

            step.update_next_index(next_index=next_index)
            next_step.update_previous_index(previous_index=index)

        return acc, boot_state


class StepExecutor:

    @staticmethod
    def execute_step(step: Step, acc: int) -> typing.Tuple[int, int]:
        executor = StepExecutor.__get_executor(step)
        return executor(step, acc)


    @staticmethod
    def __get_executor(step: Step):
        if step.command == Command.nop:
            return StepExecutor.__execute_nop
        elif step.command == Command.acc:
            return StepExecutor.__execute_acc
        elif step.command == Command.jmp:
            return StepExecutor.__execute_jmp

    @staticmethod
    def __execute_nop(step: Step, acc: int) -> typing.Tuple[int, int]:
        return step.index + 1, acc

    @staticmethod
    def __execute_acc(step: Step, acc: int) -> typing.Tuple[int, int]:
        return step.index + 1, acc + step.command_value

    @staticmethod
    def __execute_jmp(step: Step, acc: int) -> typing.Tuple[int, int]:
        return step.index + step.command_value, acc


def fix_boot(steps: typing.List[Step], index: int) -> (typing.List[Step], bool):
    step = steps[index]
    has_changed = False

    if step.command == Command.jmp:
        step.command = Command.nop
        has_changed = True
    elif step.command == Command.nop:
        step.command = Command.jmp
        has_changed = True

    return steps, has_changed


def main(input_list: typing.List[str]):
    step_converter = StepConveter()

    terminated_reasom = None
    index = 0

    while terminated_reasom != BootState.Terminate and index < len(input_list):

        steps = step_converter.convert_steps(input_list)
        steps, has_changed = fix_boot(steps, index)

        index += 1
        if not has_changed:
            continue

        acc, term_reason = step_converter.link_steps(steps)

        terminated_reasom = term_reason
        if term_reason == BootState.Terminate:
            print('Acc: {}, termination reason: {}'.format(acc, term_reason))
            break
