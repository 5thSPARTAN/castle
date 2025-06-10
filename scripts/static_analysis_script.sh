#!/bin/bash

SCRIPT_FOLDER="../src/*"
CHECKS="*, -llvmlibc-*, -modernize-use-trailing-return-type, -readability-identifier-length, -fuchsia-default-arguments-calls, -cppcoreguidelines-avoid-magic-numbers, -bugprone-easily-swappable-parameters, -readability-magic-numbers, -readability-use-anyofallof"

CLEAN_CHECKS="*, -llvmlibc-*, -modernize-use-trailing-return-type, -readability-identifier-length, -fuchsia-default-arguments-calls, -cppcoreguidelines-avoid-magic-numbers, -bugprone-easily-swappable-parameters, -readability-magic-numbers, -readability-use-anyofallof, -altera-unroll-loops, -misc-include-cleaner, -readability-function-cognitive-complexity, -altera-id-dependent-backward-branch"


for file in $SCRIPT_FOLDER
do
    if [[ "$file" == *.cpp && $file != */main.cpp ]]; then
        echo "Reading $file ..."
        #clang-tidy $file -checks="$CLEAN_CHECKS" -quiet
        clang-tidy $file -checks="$CLEAN_CHECKS" -warnings-as-errors='*' -quiet
    fi
done