#-----------------------------------------------------------------
# casescore: casescore.py
#
# Given a C (c99) code, this package classifies the identifiers
# by naming style into different groups and computes the 
# frequency distribution of each group.
#
# Copyright (C) 2014, Arun Saha
# License: BSD
#-----------------------------------------------------------------

from __future__ import print_function
from enum import Enum
from pprint import pprint
from subprocess import call
import collections
import sys
import subprocess

sys.path.append( './external/pycparser' )
try:
    from pycparser import c_parser, c_ast, parse_file
except ImportError:
    print( "**** Please run './make_all.sh' first *****" )
    sys.exit( 0 )

__version__ = '0.01'

# Portable cpp path for Windows and Linux/Unix
CPPPATH = '../utils/cpp.exe' if sys.platform == 'win32' else 'cpp'

# C Compiler
CC = 'gcc'

# Enum/Class to model string classification, see utstrclass
class Case( Enum ):
    Unknw = 0
    Lower = 1
    Upper = 2
    LowUn = 3
    UppUn = 4
    Camel = 5
    Mixed = 6

def casename( caseenum ):
    cnd = {}    # case name dict
    cnd[ Case.Unknw ] = "Unknown"
    cnd[ Case.Lower ] = "Lower"
    cnd[ Case.Upper ] = "Upper"
    cnd[ Case.LowUn ] = "LowerUnderscore"
    cnd[ Case.UppUn ] = "UpperUnderscore"
    cnd[ Case.Camel ] = "Camel"
    cnd[ Case.Mixed ] = "Mixed"
    return cnd[ caseenum ]

# Input: String
# Output: counts of lower, upper, underscore as tuple
def casecount( str ):
    n = len( str )
    nLower = 0
    nUpper = 0
    nUnderscore = 0
    for i in range( 0, n ):
        ch = str[ i ]
        nLower += 1 if ch.islower() else 0
        nUpper += 1 if ch.isupper() else 0
        nUnderscore += 1 if ch == '_' else 0
    return (nLower, nUpper, nUnderscore)

# Input: counts of lower, upper, underscore
# Output: Case.* enum
def classify( nLo, nUp, nUn ):
    if nLo >= 0 and nUp == 0 and nUn == 0:
        return Case.Lower
    elif nLo == 0 and nUp > 0 and nUn == 0:
        return Case.Upper
    elif nLo > 0 and nUp == 0 and nUn > 0:
        return Case.LowUn
    elif nLo == 0 and nUp > 0 and nUn > 0:
        return Case.UppUn
    elif nLo > 0 and nUp > 0 and nUn == 0:
        return Case.Camel
    elif nLo > 0 and nUp > 0 and nUn > 0:
        return Case.Mixed
    else:
        return Case.Unknw

# Input: String
# Output: Case.* enum
def strclass( str ):
    return classify( *casecount( str ) )

def utstrclass():
    utdict = {
        "abcd"  : Case.Lower,
        "ABCD"  : Case.Upper,
        "abcd_" : Case.LowUn,
        "ABCD_" : Case.UppUn,
        "abAB"  : Case.Camel,
        "ab_AB" : Case.Mixed
    }
    for key in utdict.keys():
        assert( strclass( key ) == utdict[ key ] )

class IdVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.idDict_ = collections.defaultdict( int )
    def visit_ID(self, node):
        # pprint(vars(node))
        # node.coord
        self.idDict_[ node.name ] += 1

def idDefs(filename):
    tmpFilename = filename + '.tmp'
    command = [CC, '-nostdinc', '-E', '-I',
        'external/pycparser/utils/fake_libc_include/', filename]
    with open(tmpFilename, 'w') as myoutfile:
        subprocess.call(command, stdout=myoutfile)
    ast = parse_file(
        tmpFilename,
        use_cpp=True,
        cpp_path=CPPPATH, 
    )
    v = IdVisitor()
    v.visit(ast)
    call(["rm", "-f", tmpFilename])
    return v.idDict_

# For each (id, freq), find the case-class of id and
# compose a list of (id, freq, idclass)
def fileclassify( filename ):
    idFreqClassList = []
    idDict = idDefs( filename )
    for item in idDict.items():
        idClass = strclass( item[ 0 ] )
        idFreqClassList.append( (item[ 0 ], item[ 1 ], idClass) )
    return idFreqClassList

def printline( n ):
    # TODO Improve
    str = ""
    for i in range( n ):
        str += "-"
    print( "%s" % (str) )

def printById( idFreqClassList ):
    printline( 80 )
    print( "%54s%10s%16s" % ("identifier", "frequency", "case" ) )
    printline( 80 )
    for elem in idFreqClassList:
        print( "%54s%10d%16s" % (elem[ 0 ], elem[ 1 ], casename( elem[ 2 ] ) ) )
    printline( 80 )

# Accumulate the frequencies grouped by case-class bucket
def freqByClass( idFreqClassList ):
    classFreqDict = collections.defaultdict( int )
    for elem in idFreqClassList:
        klass = elem[ 2 ]
        freq = elem[ 1 ]
        classFreqDict[ klass ] += freq
    return classFreqDict

def printByClass( classFreqDict ):
    printline( 80 )
    print( "%16s%10s" % ("case", "frequency") )
    printline( 80 )
    for item in classFreqDict.items():
        itemcasename = casename( item[ 0 ] )
        itemfreq = item[ 1 ]
        print( "%16s%10d" % (itemcasename, itemfreq) )
    printline( 80 )

def main():
    # Just Unit Test
    utstrclass()
    # Real Work
    if len( sys.argv ) > 1:
        filename = sys.argv[ 1 ]
    else:
        filename = 'test/minmax.c'
    idFreqClassList = fileclassify( filename )
    printById( idFreqClassList )
    classFreqDict = freqByClass( idFreqClassList )
    printByClass( classFreqDict )

if __name__ == "__main__":
    main()
