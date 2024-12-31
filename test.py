import requests

# Base URL
BASE = "http://127.0.0.1:5000"

# Add
response = requests.post(BASE + "/api/data", json={
    "sepal_length": 1.23,
    "sepal_width": 4.56,
    "petal_length": 2.34,
    "petal_width": 5.67,
    "category": 2
})
print(response.json())

# Get all
response = requests.get(BASE + "/api/data")
print(len(response.json()))

# Delete

record_id = 1  # Replace with the ID to delete
response = requests.delete(BASE + f"/api/data/{record_id}")
print(response.json())

# Predict
response = requests.get(BASE + "/api/predictions?sepal_length=1.23&sepal_width=4.56&petal_length=2.34&petal_width=5.67")
print(response.json())


