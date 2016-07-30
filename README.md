# casescore

Given a C (c99) code, this package classifies the identifiers
by naming style into different groups and computes the 
frequency distribution of each group.

# License
BSD

# Identifier groups with example

    Group name        Example
    -------------------------------------
    Lower             abcd
    Upper             ABCD
    LowerUnderscore   ab_cd, ab_cd_
    UpperUnderscore   AB_CD
    Camel             abAb, AbAb
    Mixed             ab_AB

# Usage example

Here is a toy source file we will demonstrate the tool with.

    $ cat test/minmax.c 
    #include <stdio.h>
    #include <limits.h>
    
    /* For purpose of testing, the variable names are intentionally weird */
    
    int min( int aNumber, int b_int ) {
        return b_int < aNumber ? b_int : aNumber;
    }
    
    int max( int a, int b ) {
        return b > a ? b : a;
    }
    
    int minrange( int const * ARR, int const arr_Length ) {
        int i = 0;
        int cur_min = INT_MAX;
        for( i = 0; i != arr_Length; ++i ) {
            int const newMin = min( cur_min, ARR[ i ] );
            cur_min = newMin < cur_min ? newMin : cur_min;
        }
        return cur_min;
    }
    
    void printmin( int a, int b ) {
        (void) a;
        (void) b;
    }
    $

The tool can be run as follows.

    $ python3 casescore.py test/minmax.c 
    --------------------------------------------------------------------------------
                                                identifier frequency            case
    --------------------------------------------------------------------------------
                                                       min         1           Lower
                                                     b_int         2 LowerUnderscore
                                                    newMin         2           Camel
                                                   cur_min         5 LowerUnderscore
                                                         i         4           Lower
                                                         a         3           Lower
                                                       ARR         1           Upper
                                                arr_Length         1           Mixed
                                                   aNumber         2           Camel
                                                         b         3           Lower
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
                case frequency
    --------------------------------------------------------------------------------
               Upper         1
               Mixed         1
               Lower        11
     LowerUnderscore         7
               Camel         4
    --------------------------------------------------------------------------------
$
