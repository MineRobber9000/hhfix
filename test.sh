#!/bin/bash

# create 256 byte file
dd if=/dev/zero of=alex.hh bs=256 count=1

# verify it's empty
printf 'before:\n'
xxd alex.hh

# apply a header
printf 'fix:\n'
python hhfix.py -t "Alex in Wonderland" -d "Apotheosis Software" -s 0x10 -1 1 -2 1 -m 1 -r 1 -c 2023 alex.hh

# verify it's correct
printf 'after:\n'
xxd alex.hh
