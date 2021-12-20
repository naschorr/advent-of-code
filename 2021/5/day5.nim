include std/prelude
include std/math
include classes

const INPUT_FILE = "input.txt"

## Plan of attack:
## - Lazy way would be to look at every line, and then check it against all previous lines for intersections.
##   O(n*(n/2)), where n is the number of lines, and n/2 is the average number of lines to check
## - Matrix for all possible vents, loop over each line and store the items in the matrix, if there's a collision,
##   record it. Θ(1,000,000) + O(n*m), where n is the number of lines and m is the average line length. 1000 x 1000 8 bit uints is
##   roughly a megabyte, so not as bad as I initially thought to store. However m could be huge, so it's hard to say.
## - HashMaps! Map the X coord to the Y coord to the count of vents at the spot. While inserting, keep track of
##   intersections so they can be refernced later. Get/set are cheap too, especially since we won't have duplicates.
##   Same O(n*m) problem as the matrix solution, but much cheaper in terms of memory.
## - Smarter hash maps? Vertical line map that maps an X coord to another (sorted) hash map of nodes (start and end,
##   where they both link back to the same line of vents). Same for horizontal line map. Inserting a line means (O(1)
##   insert into first map, and then 2 inserts O(n) each into the second map). Upon insert, collisions can be found by
##   checking all maps spanning the breadth of the line. If it's a vertical line then all of the horizontal lines
##   between the range (inclusive) and then the single vertical line map. (O(n*m) + O(o))). Collisions are tracked upon
##   insertion for easy retrieval later.

## Basic hash map implementation (the third one) for this solution, gonna keep it simple

class VentLine:
    var x1: int
    var y1: int
    var x2: int
    var y2: int

    method getLength(): int =
        ## Sort of unsafe conversion, but we're dealing with integer, linear coordinates so it's fine.
        return int( sqrt( float((this.x2 - this.x1) ^ 2 + (this.y2 - this.y1) ^ 2) ) )

    method isVertical(): bool =
        return this.x1 == this.x2

    method isHorizontal(): bool =
        return this.y1 == this.y2

class VentMapper:
    var map: Table[int, CountTable[int]] = Table[int, CountTable[int]()]()
    var overlapMap: Table[int, CountTable[int]] = Table[int, CountTable[int]()]()
    var overlaps: int = 0

    method insertCoordsAndCalculateOverlaps(x: int, y: int) =
        if (not this.map.hasKey(x)):
            this.map[x] = CountTable[int]()

        let count = this.map[x][y]

        this.map[x].inc(y)
        
        if (this.map[x][y] > count and count >= 1):
            if (not this.overlapMap.hasKey(x)):
                this.overlapMap[x] = CountTable[int]()

            this.overlapMap[x].inc(y)

            if (count == 1):
                this.overlaps += 1

    method addVent*(ventLine: VentLine) =
        if (ventLine.isVertical()):
            let x = ventLine.x1
            for y in min(ventLine.y1, ventLine.y2) .. max(ventLine.y1, ventLine.y2):
                this.insertCoordsAndCalculateOverlaps(x, y)

        if (ventLine.isHorizontal()):
            let y = ventLine.y1
            for x in min(ventLine.x1, ventLine.x2) .. max(ventLine.x1, ventLine.x2):
                this.insertCoordsAndCalculateOverlaps(x, y)


let ventMapper = VentMapper()

for line in lines(INPUT_FILE):
    let tokens = line.split({' ', ','})
    
    let x1 = parseInt(tokens[0])
    let y1 = parseInt(tokens[1])
    let x2 = parseInt(tokens[3])
    let y2 = parseInt(tokens[4])

    let ventLine = VentLine(x1: x1, y1: y1, x2: x2, y2: y2).init()
    ventMapper.addVent(ventLine)

echo fmt"Part one: {ventMapper.overlaps}"