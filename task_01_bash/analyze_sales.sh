#!/usr/bin/env bash

# analyze_sales.sh
# Usage: ./analyze_sales.sh sales.txt
# Format: date weekday product price quantity

if [ $# -lt 1 ]; then
  echo "Ошибка: не указан файл." >&2
  echo "Использование: $0 <sales_file>" >&2
  exit 1
fi

file="$1"

if [ ! -f "$file" ]; then
  echo "Ошибка: файл '$file' не найден." >&2
  exit 1
fi

if [ ! -r "$file" ]; then
  echo "Ошибка: файл '$file' недоступен для чтения." >&2
  exit 1
fi

# Sum price*quantity for all rows.
# Awk supports floating point numbers.
total=$(awk '
  NF==0 { next }                       # skip empty lines
  $4 ~ /^[0-9]+(\.[0-9]+)?$/ && $5 ~ /^[0-9]+$/ {
    sum += $4 * $5
    next
  }
  { bad++ }                            # count bad lines (optional)
  END {
    # print without trailing zeros if integer, else keep decimals
    if (sum == int(sum)) printf "%d", sum
    else printf "%.2f", sum
  }
' "$file")

echo "Общая сумма продаж: $total"

