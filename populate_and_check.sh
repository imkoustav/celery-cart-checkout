#!/bin/bash

# Add user
curl -s -X POST http://localhost:5000/user \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "name": "Test User"}' > /dev/null

# Add items
for i in {101..105}; do
  curl -s -X POST http://localhost:5000/item \
       -H "Content-Type: application/json" \
       -d "{\"id\": $i, \"name\": \"Item $i\", \"price\": $((RANDOM % 100 + 1)).99}" > /dev/null
done

# Add to cart
for i in {101..105}; do
  curl -s -X POST http://localhost:5000/cart/add \
       -H "Content-Type: application/json" \
       -d "{\"user_id\": 1, \"item_id\": $i, \"quantity\": $((RANDOM % 5 + 1))}" > /dev/null
done

# Trigger multiple checkouts
for i in {1..3}; do
  curl -s -X POST http://localhost:5000/checkout \
       -H "Content-Type: application/json" \
       -d '{"user_id": 1}' > /dev/null
done

# Wait for async processing to complete
echo "Waiting for background processing..."
sleep 5

# Fetch metrics
echo -e "\n===== METRICS ====="
curl -s http://localhost:5000/metrics | jq .
