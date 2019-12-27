DATA_FILEPATH = "data.txt"


class IntcodeInstruction:
    def __init__(self, processor, opcode, parameter_count, mutates_intcodes, operation):
        self.processor = processor
        self.opcode = opcode
        self.parameters = self._get_parameters(parameter_count)
        self.parameter_modes = self._parse_parameter_modes()
        self.mutates_intcodes = mutates_intcodes
        self.operation = operation


    def __len__(self):
        return 1 + len(self.parameters)


    def _get_parameters(self, count):
        parameters = []

        for index in range(count):
            parameters.append(self.processor.active_intcode[self.processor.instruction_pointer + 1 + index])

        return parameters


    def _parse_parameter_modes(self):
        parameter_modes = []
        instruction = self.opcode // 100

        while (instruction > 0 or len(parameter_modes) < len(self.parameters)):
            ## todo: enforce correct parameter mode? Must be 0 or 1
            ## Insert parameters modes in same order as parameters. This will also pad 0s onto the end such that ever
            ## parameter will have an associated parameter mode (defaulting to position mode)
            parameter_modes.append(instruction % 10)
            instruction //= 10

        return parameter_modes


    def _process_parameters(self):
        processed_parameters = []

        ## Convert any position mode params into immediate params
        for index, (parameter, mode) in enumerate(zip(self.parameters, self.parameter_modes)):
            if (mode == 1 or index == len(self.parameters) - 1 and self.mutates_intcodes):
                processed_parameters.append(parameter)
            else:
                processed_parameters.append(self.processor.active_intcode[parameter])

        return processed_parameters


    def execute(self):
        processed_parameters = self._process_parameters()
        self.operation(*processed_parameters)


class IntcodeProcessor:
    def __init__(self):
        self.active_intcode = []
        self.instruction_pointer = 0


    def _add(self, left, right, position):
        self.active_intcode[position] = left + right


    def _multiply(self, left, right, position):
        self.active_intcode[position] = left * right


    def _input(self, position):
        value = int(input('Input: '))
        self.active_intcode[position] = value


    def _output(self, value):
        print(value)


    def _jump_if_true(self, value, position):
        if (value != 0):
            self.instruction_pointer = position


    def _jump_if_false(self, value, position):
        if (value == 0):
            self.instruction_pointer = position


    def _less_than(self, left, right, position):
        if (left < right):
            self.active_intcode[position] = 1
        else:
            self.active_intcode[position] = 0


    def _equals(self, left, right, position):
        if (left == right):
            self.active_intcode[position] = 1
        else:
            self.active_intcode[position] = 0


    def _parse_instruction(self, instruction):
        opcode = instruction % 100

        if (opcode == 1):
            return IntcodeInstruction(self, instruction, 3, True, self._add)
        elif (opcode == 2):
            return IntcodeInstruction(self, instruction, 3, True, self._multiply)
        elif (opcode == 3):
            return IntcodeInstruction(self, instruction, 1, True, self._input)
        elif (opcode == 4):
            return IntcodeInstruction(self, instruction, 1, False, self._output)
        elif (opcode == 5):
            return IntcodeInstruction(self, instruction, 2, False, self._jump_if_true)
        elif (opcode == 6):
            return IntcodeInstruction(self, instruction, 2, False, self._jump_if_false)
        elif (opcode == 7):
            return IntcodeInstruction(self, instruction, 3, True, self._less_than)
        elif (opcode == 8):
            return IntcodeInstruction(self, instruction, 3, True, self._equals)
        elif (opcode == 99):
            return None
        else:
            print("Something's gone horribly wrong! Invalid opcode: {}".format(opcode))
            return None


    def process_intcodes(self, intcodes):
        self.active_intcode = intcodes.copy()

        self.instruction_pointer = 0
        while (self.instruction_pointer < len(self.active_intcode)):
            instruction = self._parse_instruction(self.active_intcode[self.instruction_pointer])
            if (instruction != None):
                last_instruction_pointer = self.instruction_pointer

                instruction.execute()

                if (self.instruction_pointer == last_instruction_pointer):
                    self.instruction_pointer += len(instruction)
            else:
                break

        return self.active_intcode.copy()


def read_data(filepath):
    with open(filepath) as fd:
        return list(map(int, fd.readline().split(',')))


def is_list_equal(a, b):
    if (len(a) != len(b)):
        return False

    for a_item, b_item in zip(a, b):
        if (a_item != b_item):
            return False

    return True


if (__name__ == '__main__'):
    intcode_processor = IntcodeProcessor()

    ## Sanity checks
    assert (is_list_equal(intcode_processor.process_intcodes([1,0,0,0,99]), [2,0,0,0,99]))
    assert (is_list_equal(intcode_processor.process_intcodes([2,3,0,3,99]), [2,3,0,6,99]))
    assert (is_list_equal(intcode_processor.process_intcodes([2,4,4,5,99,0]), [2,4,4,5,99,9801]))
    assert (is_list_equal(intcode_processor.process_intcodes([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99]))
    assert (is_list_equal(intcode_processor.process_intcodes([1101,5,5,0,99]), [10,5,5,0,99]))
    assert (is_list_equal(intcode_processor.process_intcodes([1001,4,1,0,99]), [100,4,1,0,99]))
    assert (is_list_equal(intcode_processor.process_intcodes([4,1,99]), [4,1,99]))

    ## Part 1 & 2
    intcodes = read_data(DATA_FILEPATH)
    results = intcode_processor.process_intcodes(intcodes)
