include std/prelude

type Vector3 = object
    x: int
    y: int
    z: int


type Submarine = object
    position: Vector3
    aim: int

func newSubmarine(): Submarine =
    result.position = Vector3(x: 0, y: 0, z: 0)
    result.aim = 0

func move_horizontal*(self: var Submarine, distance: int) =
    self.position.x += distance
    self.position.z += self.aim * distance

func rise*(self: var Submarine, distance: int) {.deprecated.} =
    self.position.z += distance

func dive*(self: var Submarine, distance: int) {.deprecated.} =
    self.position.z -= distance

func aim_up*(self: var Submarine, distance: int) =
    self.aim -= distance

func aim_down*(self: var Submarine, distance: int) =
    self.aim += distance


var submarine = Submarine()
for line in lines("input.txt"):
    var data: seq[string] = split(line, " ")
    let command = toLowerAscii(data[0])
    let magnitude = parseInt(data[1])

    if (command == "forward"):
        submarine.move_horizontal(magnitude)
    elif (command == "up"):
        ## submarine.rise(magnitude)
        submarine.aim_up(magnitude)
    elif (command == "down"):
        ## submarine.dive(magnitude)
        submarine.aim_down(magnitude)
    else:
        echo fmt"Unknown command: '{command}', with magnitude: '{magnitude}'. Raw: '{line}'."

## Part one's answer was '1924923'
let answer = submarine.position.x * submarine.position.z
echo fmt"Answer: '{answer}'"
