import std/sequtils
import std/strutils
import std/math


proc readInput[T](filename: string, mapper: proc(s: string): T): seq[T] =
    var data: seq[T] = @[]
    for line in lines(filename):
        data.add(mapper(line))

    return data


proc countMeasurementDepthIncreases(data: seq[int]): int =
    if (data.len() <= 1):
        return 0

    var counter = 0
    var lastDepth = data[0]
    for datum in data[1 .. data.len() - 1]:
        if (datum > lastDepth):
            counter += 1
        lastDepth = datum
    
    return counter


proc countMeasurementWindowSumIncreases(data: seq[int], windowSize: int = 3): int =
    if (data.len() < windowSize):
        return 0

    var counter = 0
    var lastSum: int = sum(data[0 .. windowSize - 1])
    for index in 1 .. data.len() - windowSize:
        var domainSum: int = sum(data[index .. index + windowSize - 1])

        if (domainSum > lastSum):
            counter += 1

        lastSum = domainSum
    
    return counter


let data = readInput("input.txt", parseInt)
echo countMeasurementDepthIncreases(data)
echo countMeasurementWindowSumIncreases(data, 3)
