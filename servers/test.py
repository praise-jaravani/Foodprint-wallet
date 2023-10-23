import requests

# Define the request payload
payload = {
    "user_id": 12345,  # Replace with the sender's user ID
    "receiver_id": 54321,  # Replace with the receiver's user ID
    "amount": 10000  # Replace with the amount to send
}

# Make a POST request to the /send_money endpoint
response = requests.post("http://localhost:8000/send_money", json=payload)

# Check the response
if response.status_code == 200:
    print("Money sent successfully")
else:
    print("Money transfer failed")
