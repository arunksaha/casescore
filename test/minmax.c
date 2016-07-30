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
