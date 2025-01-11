import requests

# Base URL
BASE = "http://127.0.0.1:5000"

# Add
print("ADD TEST \n")
response = requests.post(BASE + "/api/data", json={
    "sepal_length": 1.23,
    "sepal_width": 4.56,
    "petal_length": 2.34,
    "petal_width": 5.67,
    "category": 2
})
print(response.json())
print("\nGETALL TEST \n")

# Get all
response = requests.get(BASE + "/api/data")
for iris in response.json():
    print(iris)

print("len:", len(response.json()))
print("\nDELETE TEST \n")

# Delete
record_id = 11
response = requests.delete(BASE + f"/api/data/{record_id}")
print(response.json())
print("\nPREDICT TEST \n")

# Predict
response = requests.get(BASE + "/api/predictions", json={
    "sepal_length": 1.23,
    "sepal_width": 4.56,
    "petal_length": 2.34,
    "petal_width": 5.67,
})
print(response.json())
