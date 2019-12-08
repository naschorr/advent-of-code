DATA_FILEPATH = "data.txt"

class IntcodeProcessor:
    def __init__(self):
        self.active_intcode = []


    def _add(self, left, right, target):
        result = self.active_intcode[left] + self.active_intcode[right]
        self.active_intcode[target] = result


    def _multiply(self, left, right, target):
        result = self.active_intcode[left] * self.active_intcode[right]
        self.active_intcode[target] = result


    def _retrieve_instruction(self):
        for index in range(0, len(self.active_intcode), 4):
            opcode = self.active_intcode[index]
            operands = ()

            if (len(self.active_intcode) >= index + 4):
                operands = (
                    self.active_intcode[index + 1],
                    self.active_intcode[index + 2],
                    self.active_intcode[index + 3]
                )

            yield (opcode, operands)


    def execute(self, intcodes):
        self.active_intcode = intcodes.copy()

        for opcode, operands in self._retrieve_instruction():
            if (opcode == 1):
                self._add(*operands)
            elif (opcode == 2):
                self._multiply(*operands)
            elif (opcode == 99):
                break
            else:
                print("Something's gone horribly wrong! Invalid opcode: {}".format(opcode))
                break

        return self.active_intcode


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


def find_solution(intcodes, solution):
    noun = None
    noun_index = 0
    while (noun is None and noun_index <= 99):
        verb = None
        verb_index = 0
        while (verb is None and verb_index <= 99):
            intcodes[1] = noun_index
            intcodes[2] = verb_index

            output = intcode_processor.execute(intcodes)
            if (output[0] == solution):
                noun = noun_index
                verb = verb_index

            verb_index += 1
        noun_index += 1

    return noun, verb


if (__name__ == '__main__'):
    intcode_processor = IntcodeProcessor()

    ## Sanity checks
    assert (is_list_equal(intcode_processor.execute([1,0,0,0,99]), [2,0,0,0,99]))
    assert (is_list_equal(intcode_processor.execute([2,3,0,3,99]), [2,3,0,6,99]))
    assert (is_list_equal(intcode_processor.execute([2,4,4,5,99,0]), [2,4,4,5,99,9801]))
    assert (is_list_equal(intcode_processor.execute([1,1,1,4,99,5,6,0,99]), [30,1,1,4,2,5,6,0,99]))

    ## Part 1
    intcodes = read_data(DATA_FILEPATH)
    intcode_processor.execute(intcodes)

    ## Part 2
    noun, verb = find_solution(intcodes, 19690720)
        
    print("Noun: {}, Verb: {}, Answer: {}".format(noun, verb, 100 * noun + verb))
                