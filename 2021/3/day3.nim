include std/prelude
include std/math
include std/bitops

type DiagnosticAccumulator = object
    ## Does Nim have a proper bit field storage object? The docs seem to say that it doesn't.
    bitMatrix: seq[seq[int]]
    zeroCounter: seq[int]
    oneCounter: seq[int]
    width: int

func newDiagnosticAccumulator*(): DiagnosticAccumulator =
    result.bitMatrix = @[]
    result.zeroCounter = @[]
    result.oneCounter = @[]
    result.width = 0

func reset*(self: var DiagnosticAccumulator) =
    ## todo: Is there a way to tell the constructor to use this reset method to keep DRY?

    self.bitMatrix = @[]
    self.zeroCounter = @[]
    self.oneCounter = @[]
    self.width = 0

func addDiagnosticLine*(self: var DiagnosticAccumulator, data: string) =
    ## Make sure the counters are long enough to support seamless insertions
    for index in self.width .. data.len() - 1:
        self.zeroCounter.add(0)
        self.oneCounter.add(0)
        self.width += 1

    var bits: seq[int] = @[]
    for index, digit in pairs(data):
        if (digit == '0'):
            self.zeroCounter[index] = self.zeroCounter[index] + 1
            bits.add(0)
        else:
            self.oneCounter[index] = self.oneCounter[index] + 1
            bits.add(1)
    
    self.bitMatrix.add(bits)

func calculatePowerConsumption*(self: DiagnosticAccumulator): int =
    ## Part one

    var gammaRate = 0
    var epsilonRate = 0

    for index, counterTuple in pairs(zip(self.zeroCounter, self.oneCounter)):
        if (counterTuple[0] < counterTuple[1]):
            gammaRate += 2 ^ (self.zeroCounter.len() - 1 - index)
        else:
            epsilonRate += 2 ^ (self.zeroCounter.len() - 1 - index)

    return gammaRate * epsilonRate

proc calculateLifeSupportRating*(self: DiagnosticAccumulator): int =
    ## todo: I'm really not proud of this, so it should really be cleaned up.

    ## Part two

    var mostCommonValueDomain: seq[seq[int]] = deepCopy(self.bitMatrix)
    var leastCommonValueDomain: seq[seq[int]] = deepCopy(self.bitMatrix)

    for index in 0 .. self.width - 1:
        ## Most Common Search

        var zeroDomain: seq[seq[int]] = @[]
        var oneDomain: seq[seq[int]] = @[]

        for bitField in mostCommonValueDomain:
            if (bitField[index] == 0):
                zeroDomain.add(bitField)
            else:
                oneDomain.add(bitField)
            
        if (zeroDomain.len() > oneDomain.len()):
            mostCommonValueDomain = zeroDomain
        else:
            mostCommonValueDomain = oneDomain

        ## Least Common Search

        zeroDomain = @[]
        oneDomain = @[]

        if (leastCommonValueDomain.len() > 1):
            for bitField in leastCommonValueDomain:
                if (bitField[index] == 0):
                    zeroDomain.add(bitField)
                else:
                    oneDomain.add(bitField)
                
            if (zeroDomain.len() <= oneDomain.len()):
                leastCommonValueDomain = zeroDomain
            else:
                leastCommonValueDomain = oneDomain

    var oxygenGeneratorRating = 0
    var co2ScrubberRating = 0

    for index, valueTuple in pairs(zip(leastCommonValueDomain[0], mostCommonValueDomain[0])):
        co2ScrubberRating += valueTuple[0] * 2 ^ (leastCommonValueDomain[0].len() - 1 - index)
        oxygenGeneratorRating += valueTuple[1] * 2 ^ (mostCommonValueDomain[0].len() - 1 - index)

    return oxygenGeneratorRating * co2ScrubberRating


var diagnosticAccumulator = DiagnosticAccumulator()

## Sanity checks

let testData = @[
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
]
for line in testData:
    diagnosticAccumulator.addDiagnosticLine(line)

assert(diagnosticAccumulator.calculatePowerConsumption() == 198)
assert(diagnosticAccumulator.calculateLifeSupportRating() == 230)

diagnosticAccumulator.reset()

## Actual solutions

for line in lines("input.txt"):
    diagnosticAccumulator.addDiagnosticLine(line)

echo fmt"Part one: {diagnosticAccumulator.calculatePowerConsumption()}"
echo fmt"Part two: {diagnosticAccumulator.calculateLifeSupportRating()}"
