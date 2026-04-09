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

awk '
  BEGIN {
    total = 0
    best_sum = -1
  }

  NF == 0 { next }  # skip empty lines

  # columns: 1 date, 2 weekday, 3 product, 4 price, 5 quantity
  $4 ~ /^[0-9]+(\.[0-9]+)?$/ && $5 ~ /^[0-9]+$/ {
    date = $1
    weekday = $2
    product = $3
    price = $4 + 0
    qty = $5 + 0

    revenue = price * qty
    total += revenue

    # day revenue (key = "date weekday")
    day_key = date " " weekday
    day_sum[day_key] += revenue

    # product popularity
    prod_qty[product] += qty
    prod_sum[product] += revenue

    next
  }

  { bad_lines++ } # ignore bad lines

  END {
    # find best day
    for (k in day_sum) {
      if (day_sum[k] > best_sum) {
        best_sum = day_sum[k]
        best_day = k
      }
    }

    # find most popular product by quantity (tie -> bigger revenue)
    best_prod = ""
    best_qty = -1
    best_prod_sum = -1

    for (p in prod_qty) {
      if (prod_qty[p] > best_qty || (prod_qty[p] == best_qty && prod_sum[p] > best_prod_sum)) {
        best_qty = prod_qty[p]
        best_prod_sum = prod_sum[p]
        best_prod = p
      }
    }

    # formatting
    # total with 2 decimals (since prices can be decimals)
    printf "Общая сумма продаж: %.2f\n", total

    if (best_day != "") {
      printf "Лучший день: %s (%.2f)\n", best_day, best_sum
    } else {
      print "Лучший день: нет данных"
    }

    if (best_prod != "") {
      printf "Самый популярный товар: %s (кол-во: %d, сумма: %.2f)\n", best_prod, best_qty, best_prod_sum
    } else {
      print "Самый популярный товар: нет данных"
    }
  }
' "$file"

