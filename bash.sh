#!/bin/bash

URL="http://127.0.0.1:5000/order"

while true; do
  customer_name="John Doe$(shuf -i 1-100 -n 1)"
  product_name="Example Product$(shuf -i 1-100 -n 1)"
  quantity=$(shuf -i 1-10 -n 1)

  json_data="{\"customer_name\":\"$customer_name\",\"product_name\":\"$product_name\",\"quantity\":$quantity}"

  curl -X POST -H "Content-Type: application/json" -d "$json_data" "$URL"

  sleep 1  # Delay between creating orders
done