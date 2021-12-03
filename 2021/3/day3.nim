include std/prelude
include std/math
include std/bitops

type DiagnosticAccumulator = object
    zeroCounter: seq[int]
    oneCounter: seq[int]

func newDiagnosticAccumulator*(): DiagnosticAccumulator =
    result.zeroCounter = @[]
    result.oneCounter = @[]

func addDiagnosticLine*(self: var DiagnosticAccumulator, data: string) =
    ## Make sure the counters are long enough to support seamless insertions
    for index in self.zeroCounter.len() .. data.len() - 1:
        self.zeroCounter.add(0)
        self.oneCounter.add(0)

    for index, digit in pairs(data):
        if (digit == '0'):
            self.zeroCounter[index] = self.zeroCounter[index] + 1
        else:
            self.oneCounter[index] = self.oneCounter[index] + 1

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


var diagnosticAccumulator = DiagnosticAccumulator()
for line in lines("input.txt"):
    diagnosticAccumulator.addDiagnosticLine(line)

echo fmt"Part one: {diagnosticAccumulator.calculatePowerConsumption()}"
