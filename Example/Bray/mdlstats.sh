#!/bin/bash
# Provides statistics on non-blank lines, words, characters
# Base values: 42 lines, 811 characters
sed 's/ //g' $1 | grep -v "^$" | grep -v "^ *#" | grep -v "^ *\/"   | wc | awk '{ print ($1 - 42) "\t" ( $3 - 811 ) }'
