import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "G1": 12,
    "G2": 14,
    "studytime": 2,
    "failures": 0,
    "absences": 4
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())