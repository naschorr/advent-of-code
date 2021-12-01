from collections import defaultdict
from math import sqrt

DATA_FILEPATH = "data.txt"

class Intersection:
    def __init__(self, x, y, wires):
        self.x = x
        self.y = y
        self.wires = wires


    def __eq__(self, other):
        if (isinstance(type(self), other)):
            ## Don't need to bother with checking for wire equality, it's just the coordinates we really need
            return (self.x == other.x and self.y == other.y)

        return False


    def __hash__(self):
        return hash((self.x, self.y, tuple(self.wires)))


class WireComponent:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance
        self.start = None
        self.end = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value


class WireIntersectionFinder:
    def _reset(self):
        self.grid = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # 3d big brain plays
        self.wires = []
        self.intersections = set()


    def _store_horizontal_component_in_grid(self, wire, wire_index, position, distance):
        x = position[0]
        y = position[1]
        direction = distance // abs(distance)

        for index in range(1, abs(distance) + 1):
            x_index = x + direction * index
            self.grid[x_index][y][wire_index] += 1

            if (len(self.grid[x_index][y].items()) > 1):
                intersected_wire_indexes = list(self.grid[x_index][y].keys())
                self.intersections.add(Intersection(x_index, y, intersected_wire_indexes))


    def _store_vertical_component_in_grid(self, wire, wire_index, position, distance):
        x = position[0]
        y = position[1]
        direction = distance // abs(distance)

        for index in range(1, abs(distance) + 1):
            y_index = y + direction * index
            self.grid[x][y_index][wire_index] += 1

            if (len(self.grid[x][y_index].items()) > 1):
                intersected_wire_indexes = list(self.grid[x][y_index].keys())
                self.intersections.add(Intersection(x, y_index, intersected_wire_indexes))


    def parse_wires(self, wire_descriptions):
        wires = []
        for wire in wire_descriptions:
            components = []
            for component in wire:
                components.append(WireComponent(component[0], int(component[1:])))
            wires.append(components)

        return wires


    def find_intersections(self, wires):
        self._reset()
        self.wires = self.parse_wires(wires)

        for wire_index, wire in enumerate(self.wires):
            position = [0, 0]
            for component in wire:
                direction = component.direction
                distance = component.distance

                component.start = position.copy()

                if (direction == 'U'):
                    self._store_vertical_component_in_grid(wire, wire_index, position, distance)
                    position[1] += distance
                elif (direction == 'R'):
                    self._store_horizontal_component_in_grid(wire, wire_index, position, distance)
                    position[0] += distance
                elif (direction == 'D'):
                    self._store_vertical_component_in_grid(wire, wire_index, position, -distance)
                    position[1] -= distance
                elif (direction == 'L'):
                    self._store_horizontal_component_in_grid(wire, wire_index, position, -distance)
                    position[0] -= distance
                else:
                    print("Uh oh! Unknown direction given: {}".format(direction))

                component.end = position.copy()

        return self.intersections, self.wires


def read_data(filepath):
    with open(filepath) as fd:
        return [line.split(",") for line in fd.readlines()]


def calculate_manhattan_distance(x, y, intersection):
    return abs(intersection.x - x) + abs(intersection.y - y)


def find_shortest_manhattan_distance(intersections):
    intersections = list(intersections)

    shortest_distance = calculate_manhattan_distance(0, 0, intersections[0])
    for intersection in intersections[1:]:
        distance = calculate_manhattan_distance(0, 0, intersection)

        if (distance < shortest_distance):
            shortest_distance = distance

    return shortest_distance


def calculate_wire_length(wire, x, y):
    def distance(x1, y1, x2, y2):
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    length = 0
    for component in wire:
        start = component.start
        end = component.end

        if (distance(*start, x, y) + distance(*end, x, y) == distance(*start, *end)):
            return length + distance(*start, x, y)
        
        length += abs(component.distance)

    return length


def calculate_intersection_distance(intersection, wires):
    length = 0
    for wire_index in intersection.wires:
        length += calculate_wire_length(wires[wire_index], intersection.x, intersection.y)
    
    return length


def find_shortest_signal_distance(intersections, wires):
    intersections = list(intersections)

    shortest_distance = calculate_intersection_distance(intersections[0], wires)
    for intersection in intersections[1:]:
        distance = calculate_intersection_distance(intersection, wires)

        if (distance < shortest_distance):
            shortest_distance = distance

    return int(shortest_distance)


if (__name__ == '__main__'):
    ## I'm not proud of any of this, and should really redo it.

    intersection_finder = WireIntersectionFinder()
    wire_descriptions = read_data(DATA_FILEPATH)

    test_wires_a = [["R8","U5","L5","D3"], ["U7","R6","D4","L4"]]
    test_wires_b = [["R75","D30","R83","U83","L12","D49","R71","U7","L72"],
                    ["U62","R66","U55","R34","D71","R55","D58","R83"]]
    test_wires_c = [["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"],
                    ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]]

    ## Sanity checks
    test_intersections, test_wires = intersection_finder.find_intersections(test_wires_a)
    assert (find_shortest_manhattan_distance(test_intersections) == 6)
    test_intersections, test_wires = intersection_finder.find_intersections(test_wires_b)
    assert (find_shortest_manhattan_distance(test_intersections) == 159)
    test_intersections, test_wires = intersection_finder.find_intersections(test_wires_c)
    assert (find_shortest_manhattan_distance(test_intersections) == 135)

    assert (find_shortest_signal_distance(*intersection_finder.find_intersections(test_wires_a)) == 40)
    assert (find_shortest_signal_distance(*intersection_finder.find_intersections(test_wires_b)) == 610)
    assert (find_shortest_signal_distance(*intersection_finder.find_intersections(test_wires_c)) == 410)

    ## Part 1

    intersections, wires = intersection_finder.find_intersections(wire_descriptions)
    manhattan_distance = find_shortest_manhattan_distance(intersections)
    print("Part 1: Shortest Manhattan distance: {}".format(manhattan_distance))

    ## Part 2

    intersections, wires = intersection_finder.find_intersections(wire_descriptions)
    signal_distance = find_shortest_signal_distance(intersections, wires)
    print("Part 2: Shortest signal distance: {}".format(signal_distance))