# import requests
# import random
# import time

# base = "http://localhost:5000"

# # Add user
# requests.post(f"{base}/user", json={"id": 1, "name": "Test User"})

# # Add items
# for i in range(101, 106):
#     requests.post(f"{base}/item", json={"id": i, "name": f"Item {i}", "price": round(random.uniform(10, 100), 2)})

# # Add to cart
# for i in range(101, 106):
#     requests.post(f"{base}/cart/add", json={"user_id": 1, "item_id": i, "quantity": random.randint(1, 5)})

# # Trigger checkouts
# for _ in range(3):
#     requests.post(f"{base}/checkout", json={"user_id": 1})

# print("Waiting for background workers...")
# time.sleep(5)

# # Print metrics
# metrics = requests.get(f"{base}/metrics").json()
# print("\n===== METRICS =====")
# print(metrics)


import requests
import random
import time

base = "http://localhost:5000"

# 1. Add user
requests.post(f"{base}/user", json={"id": 1, "name": "Test User"})

# 2. Add items
for i in range(101, 156):
    requests.post(f"{base}/item", json={
        "id": i,
        "name": f"Item {i}",
        "price": round(random.uniform(10, 100), 2)
    })

# 3. Add items to cart
for i in range(101, 156):
    requests.post(f"{base}/cart/add", json={
        "user_id": 1,
        "item_id": i,
        "quantity": random.randint(1, 5)
    })

# 4. Trigger multiple checkouts (e.g. 10 total)
for _ in range(5):
    requests.post(f"{base}/checkout", json={"user_id": 1})
    time.sleep(0.2)  # slight delay between checkouts

# 5. Sleep a short time (less than worker needs to finish all)
print("Waiting briefly (some checkouts will remain pending)...")
time.sleep(2)  # intentionally short

# 6. Check metrics
metrics = requests.get(f"{base}/metrics").json()
print("\n===== METRICS =====")
print(metrics)
