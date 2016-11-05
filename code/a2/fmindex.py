#! /usr/bin/env python
# Modified from Ben Langmead's code in his teaching materials
# http://www.langmead-lab.org/teaching-materials/
import argparse

def naiveOcc(bw):
    ''' Given BWT string bw, return the occurrence array Occ[i][a]
        where Occ[i][a] is the number of times a occurs in BWT[0, i]
        Also returns tots: map from character to # times it appears. '''
    tots = {}
    for c in bw:
        tots[c] = 0
    ranks = []
    for (i, c) in enumerate(bw):
        tots[c] += 1
        ranks.append(dict(tots))
    return ranks, tots

def firstCol(tots):
    ''' Return map from character to the range of rows prefixed by
        the character. '''
    first = {}
    totc = 0
    
    for c, count in sorted(tots.iteritems()):
        first[c] = (totc, totc + count)
        totc +=  count
    return  first

def count(S, occ, C):

    # Initialize the suffix array interval [l,u] to the range containing suffixes
    # starting with the last base of the pattern S 
    i = len(S) - 1
    a = S[i]
    l = C[a][0]
    u = C[a][1] - 1
    
    if args.debug:
        print i, S[i:], l,u
    
    i -= 1
    while i >= 0:
        a = S[i] 
        # Refine the suffix array interval by updating [l,u]
        # These are determined by looking up the start/end of the interval for character a
        # and offseting it by the rank of a from the previous interval
        l = C[a][0] + occ[l - 1][a]
        u = C[a][0] + occ[u][a] - 1
        if args.debug:
            print i, S[i:], l,u, u - l + 1
        i -= 1
    return u - l + 1


# Load the BWT from disk
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bwt", type=str, help="The file containing the BWT string", required=True)
parser.add_argument("-d", "--debug", action="store_true", help="Turn on debugging information")
parser.add_argument("-c", "--count", type=str, help="The string to count", required=True)
args = parser.parse_args()

# Read the bwt string from the input file
bwt = open(args.bwt).read().replace('\n','')

# Calculate Occ(i, a) for all i 
ranks, tots = naiveOcc(bwt)

# Calculate the F column from the total character counts
F = firstCol(tots)

# Count the number of occurrences of the input string
print "%s occurs %d times" % (args.count, count(args.count, ranks, F))
