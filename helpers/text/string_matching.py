from __future__ import generators

def naiveMatch(pattern, text):
    for startPos in range(len(text) - len(pattern) + 1):
        matchLen = 0
        while pattern[matchLen] == text[startPos + matchLen]:
            matchLen += 1
            if matchLen == len(pattern):
                return startPos

def kmpFirstMatch(pattern, text):
    shift = computeShifts(pattern)
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen >= 0 and pattern[matchLen] != c:
            startPos += shift[matchLen]
            matchLen -= shift[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            return startPos

def kmpAllMatches(pattern, text):
    shift = computeShifts(pattern)
    startPos = 0
    matchLen = 0
    for c in text:
	    while matchLen >= 0 and pattern[matchLen] != c:
		    startPos += shift[matchLen]
		    matchLen -= shift[matchLen]
	    matchLen += 1
	    if matchLen == len(pattern):
		    yield startPos
		    startPos += shift[matchLen]
		    matchLen -= shift[matchLen]

def computeShifts(pattern):
    shifts = [None] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern) + 1):
        while shift < pos and pattern[pos - 1] != pattern[pos - shift - 1]:
            shift += shifts[pos - shift - 1]
        shifts[pos] = shift
    return shifts

def countAllMatches(pattern, text):
    shift = computeShifts(pattern)
    startPos = 0
    matchLen = 0
    count = 0
    for c in text:
        while matchLen >= 0 and pattern[matchLen] != c:
            startPos += shift[matchLen]
            matchLen -= shift[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            count += 1
            startPos += shift[matchLen]
            matchLen -= shift[matchLen]
    return count
    