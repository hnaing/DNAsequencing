import sys, re

def fileNum(argv):
    """Returns the input file number."""
    txt = argv[0]
    num = re.findall(r'\d+', txt)
    return int(num[0])

def readFile(argv):
    """Returns the lines from input file."""
    with open(argv[0], 'r') as f:
        lines = [line.rstrip() for line in f]
    f.close()
    return lines

def writeFile(seq, n):
    """creates an output file"""
    f = open("output%d.txt" % n, 'w')
    f.write(seq+'\n')
        
    f.close()

def overlap(seq1, seq2):
    """ Returns length of overlapping seq in seq1+seq2 and
        the index in seq1 of the first match"""
    len2 = len(seq2)
    for i in range(len(seq1)):
        len1 = len(seq1[i:])
        if len1 < len2:
            if seq1[i:] == seq2[:len1]:
                return len1, i 
        else:
            if seq1[i:i+len2] == seq2:
                return len2, i
    return 0, None

def findOverlaps(lines):
    """ Returns table of nxn that holds overlapping seq's (length,startIndexOfSeq1)
        and the index of longest overlap (or the length value)."""
    overlaps = {}
    for j,seq2 in enumerate(lines):
        for i,seq1 in enumerate(lines):
            if i != j: # if not the same seq(which means all match)
                length, index = overlap(seq1, seq2)
                if length != 0:
                    if length in overlaps:
                        overlaps[length].append(((i,j), index))
                    else:
                        overlaps[length] = [((i,j), index)]
    return overlaps # (1,2), 3: lines[1] & lines[2] overlaps starting at index 3 of lines[1]




def merge(seq1, seq2, index):
    # print seq1, seq2
    newline = seq1[:index] + seq2
    if len(newline) < len(seq1):
        return seq1
    return newline


def buildSeq(lines):

    threshold = 10

    while len(lines) > 1:
        overlaps = findOverlaps(lines) # {25: [((1,0), 2), ((#,#), #), ...], 27: [],}
        lengths = overlaps.keys()
        lengths.sort(reverse=True)
        newlines = []

        notmerged = set(range(len(lines)))
        for l in lengths:
            if l > threshold:
                vals = overlaps[l]
                for item in vals:
                    seqs, ind = item
                    if (seqs[0] in notmerged) and (seqs[1] in notmerged):
                        newlines.append(merge(lines[seqs[0]], lines[seqs[1]], ind))
                        notmerged.remove(seqs[0])
                        notmerged.remove(seqs[1])

        
        for i in notmerged:
            newlines.append(lines[i])

        if len(lines) == len(newlines):
            threshold -= 1

        # print threshold
        # print len(lines), len(newlines)
        lines = newlines

    return lines[0]




if __name__ == "__main__":
    filenum = fileNum(sys.argv[1:])
    lines = readFile(sys.argv[1:])
    from time import time
    start = time()
    built = buildSeq(lines)
    end = time()
    writeFile(built, filenum)
    print "It took %f" % (end - start)



    # lines = sys.stdin.read().splitlines()
    # built = buildSeq(lines)
    # print built
    
    # writeFile(built, filenum)