#!/bin/bash

PROGRAM="../build/testCastle"         # Path to the executable, relative to build/
ARGS=""                        # Any command-line arguments, if needed
VALGRIND_LOG="valgrind_output.log"

i=0
while true; do
    clear
    echo "🔁 Run #$i"
    valgrind --leak-check=full --track-origins=yes --log-file="$VALGRIND_LOG" $PROGRAM $ARGS
   if [ $EXIT_CODE -ne 0 ]; then
	echo "Valground found an error on run $i"
	echo "Showing valgrind output:"
	cat "$VALGRIND_LOG"
	break
   elif grep -q "depends on uninitialised value" "$VALGRIND_LOG"; then
        echo "Uninitialized value usage found on run #$i"
        echo "Showing valgrind output:"
        cat "$VALGRIND_LOG"
        break
    else
        echo "No uninitialized value issue detected. Continuing..."
    fi

    ((i++))
done
