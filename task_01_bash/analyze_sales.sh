#!/usr/bin/env bash

# analyze_sales.sh
# Usage: ./analyze_sales.sh sales.txt
# Format in sales.txt:
# date weekday product price quantity

if [ $# -lt 1 ]; then
  echo "Ошибка: нужно указать файл с продажами"
  exit 1
fi

file="$1"

if [ ! -f "$file" ]; then
  echo "Ошибка: файл '$file' не найден"
  exit 1
fi

total=0

# читаем файл построчно
while read date weekday product price quantity; do
  # пропускаем пустые строки
  [ -z "$date" ] && continue

  # простая проверка, что price и quantity не пустые
  if [ -z "$price" ] || [ -z "$quantity" ]; then
    echo "Предупреждение: пропускаю строку (нет price или quantity): $date $weekday $product $price $quantity"
    continue
  fi

  # считаем сумму
  total=$(( total + price * quantity ))

done < "$file"

echo "Общая сумма продаж: $total"

