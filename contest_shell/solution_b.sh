#!/usr/bin/env bash
set -euo pipefail

in="input.txt"
out="output.txt"

# N students
N=$(head -n 1 "$in" | tr -d '\r')

# sort mode is the last line
mode=$(tail -n 1 "$in" | tr -d '\r')

# students are lines 2..N+1
students=$(mktemp)
tail -n +2 "$in" | head -n "$N" | tr -d '\r' > "$students"

# Output format requires: "Name Surname d.m.y"
# We'll sort using hidden keys then strip them.

if [[ "$mode" == "date" ]]; then
  # key: yyyy mm dd surname name
  # input: Name Surname d m y
  LC_ALL=C awk '
    {
      name=$1; surname=$2; d=$3; m=$4; y=$5;
      printf "%04d %02d %02d %s %s %s %s %d.%d.%d\n", y, m, d, surname, name, name, surname, d, m, y
    }
  ' "$students" \
  | LC_ALL=C sort \
  | cut -d' ' -f6- > "$out"

elif [[ "$mode" == "name" ]]; then
  # key: surname name yyyy mm dd
  LC_ALL=C awk '
    {
      name=$1; surname=$2; d=$3; m=$4; y=$5;
      printf "%s %s %04d %02d %02d %s %s %d.%d.%d\n", surname, name, y, m, d, name, surname, d, m, y
    }
  ' "$students" \
  | LC_ALL=C sort \
  | cut -d' ' -f6- > "$out"

else
  # If unexpected mode, produce empty output (or you can write an error, but contest expects only output.txt)
  : > "$out"
fi

rm -f "$students"