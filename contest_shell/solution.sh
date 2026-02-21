#!/usr/bin/env bash

in="input.txt"
out="output.txt"

letters=$(grep -oE '[A-Za-z]' "$in" | wc -l | tr -d ' ')
words=$(wc -w < "$in" | tr -d ' ')
lines=$(wc -l < "$in" | tr -d ' ')

{
  echo "Input file contains:"
  echo "$letters letters"
  echo "$words words"
  echo "$lines lines"
} > "$out"
