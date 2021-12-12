include std/prelude
include std/math

const INPUT_FILE = "input.txt"
const BINGO_BOARD_SIZE = 5

type BingoItem = object
    value: int
    x: int
    y: int
    marked: bool

proc markItem(self: var BingoItem) =
    self.marked = true

type BingoBoard = object
    items: Table[int, BingoItem]
    markedItems: HashSet[int]
    unmarkedItems: HashSet[int]
    board: seq[seq[int]]

proc newBingoBoard(rawData: var seq[string]): BingoBoard =
    ## Assumes that it's given the raw strings comprising the board input
    result.board = @[]
    result.items = Table[int, BingoItem]()
    result.markedItems = HashSet[int]()
    result.unmarkedItems = HashSet[int]()
    for yIndex, line in pairs(rawData):
        var row: seq[int] = @[]
        for xIndex, item in pairs(line.splitWhitespace()):
            let value = parseInt(item)

            row.add(value)
            var bingoItem = BingoItem(value: value, x: xIndex, y: yIndex, marked: false)
            result.items[value] = bingoItem
            result.unmarkedItems.incl(value)

        result.board.add(row)

proc checkBingos(self: BingoBoard, value: int): bool =
    ## We know that the provided integer maps to a marked item on the board, so check it's neighbors in a vertical line
    ## and/or a horizontal line

    if (value in self.items):
        let item = self.items[value]

        ## Check for vertical bingos
        ## We know the coordinates of the freshly marked item, so check all of the items in that column for their marked
        ## status. If one hasn't been marked then clearly there isn't a vertical bingo. Technically this could be split
        ## out into two loops to check before and after the freshly marked item, but I think that just adds ugly
        ## complexity for very little performance gain. (O(n) vs O(n-1))
        var verticalBingo = true
        for yIndex in 0 .. BINGO_BOARD_SIZE - 1:
            if (not self.items[self.board[yIndex][item.x]].marked):
                verticalBingo = false
                break

        if (verticalBingo):
            return true

        ## Check horizontal bingos
        var horizontalBingo = true
        for xIndex in 0 .. BINGO_BOARD_SIZE - 1:
            if (not self.items[self.board[item.y][xIndex]].marked):
                horizontalBingo = false
                break

        return horizontalBingo

proc markItem(self: var BingoBoard, value: int) =
    if (value in self.items):
        self.items[value].markItem();
        self.markedItems.incl(value)
        self.unmarkedItems.excl(value)


proc main() =
    var bingoNumbers: seq[int] = @[]
    var bingoBoards: seq[BingoBoard] = @[]
    var bingoBoardData: seq[string] = @[]
    for line in lines(INPUT_FILE):
        if (line == ""):
            continue

        ## Only handle the bingo numbers if they haven't already been loaded. They come first in the input, so this is
        ## really just a lazy one-and-done.
        if (bingoNumbers.len() == 0):
            bingoNumbers = map(line.split(","), parseInt)
            continue

        bingoBoardData.add(line)
        if (bingoBoardData.len() == BINGO_BOARD_SIZE):
            bingoBoards.add(newBingoBoard(bingoBoardData))
            bingoBoardData = @[]


    var bingoFound = false
    var bingoNumberIndex = 0
    while (not bingoFound and bingoNumberIndex < bingoNumbers.len()):
        let number = bingoNumbers[bingoNumberIndex]
        for index, board in mpairs(bingoBoards):
            board.markItem(number)

            ## Does nim short circuit conditionals? Also a bingo is impossible if 4 or fewer numbers have been drawm, so
            ## skip the check
            if (bingoNumberIndex > 4 and board.checkBingos(number)):
                var unmarkedItemsSum: int = sum(board.unmarkedItems.toSeq())
                echo fmt("Part one: {unmarkedItemsSum * number}")
                bingoFound = true
                break
        
        bingoNumberIndex += 1

main()
