import requests
import time
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"
user_email = "admin@kavan.local"

print("--- TEST 1: REJECT INVALID TOKEN ---")
res = requests.post(f"{BASE_URL}/auth/reset-password/", json={
    "token": "totally_made_up_token_123",
    "password": "NewStrongP@ssw0rd!",
    "confirm_password": "NewStrongP@ssw0rd!"
})
if res.status_code == 400 and "Invalid or expired token" in res.text:
    print("SUCCESS: Rejected invalid token with error:", res.json().get('errors'))
else:
    print("FAIL: Accepted invalid token?! Response:", res.status_code, res.text)

print("\n--- TEST 2: GENERATE AND USE REAL TOKEN ---")
# Trigger forgot password
res = requests.post(f"{BASE_URL}/auth/forgot-password/", json={"email": user_email})
if res.status_code == 200:
    print("Forgot password triggered successfully.")
else:
    print("Failed to trigger forgot password:", res.status_code, res.text)

# Give the server a moment to write the token file
time.sleep(2)

with open("C:\\Users\\purus\\Documents\\praveen broo\\kavan\\backend\\test_token_abs.txt", "r") as f:
    token = f.read().strip()
print(f"Token read from file: {token}")

res = requests.post(f"{BASE_URL}/auth/reset-password/", json={
    "token": token,
    "password": "Admin123!New12345",
    "confirm_password": "Admin123!New12345"
})
if res.status_code == 200:
    print("SUCCESS: Password reset successfully using valid token.")
else:
    print("FAIL: Could not reset password:", res.status_code, res.text)

print("\n--- TEST 3: REJECT USED TOKEN ---")
res = requests.post(f"{BASE_URL}/auth/reset-password/", json={
    "token": token,
    "password": "Admin123!New54321",
    "confirm_password": "Admin123!New54321"
})
if res.status_code == 400 and "Token has already been used" in res.text:
    print("SUCCESS: Rejected used token with error:", res.json().get('errors'))
else:
    print("FAIL: Accepted used token?! Response:", res.status_code, res.text)

print("\n--- TEST 4: CLEANUP (Revert password) ---")
res = requests.post(f"{BASE_URL}/auth/forgot-password/", json={"email": user_email})
time.sleep(2)
with open("C:\\Users\\purus\\Documents\\praveen broo\\kavan\\backend\\test_token_abs.txt", "r") as f:
    revert_token = f.read().strip()

res = requests.post(f"{BASE_URL}/auth/reset-password/", json={
    "token": revert_token,
    "password": "Admin123!",
    "confirm_password": "Admin123!"
})
if res.status_code == 200:
    print("SUCCESS: Password reverted to original.")
else:
    print("FAIL: Could not revert password:", res.status_code, res.text)

# Cleanup the test token file
try:
    os.remove("C:\\Users\\purus\\Documents\\praveen broo\\kavan\\backend\\test_token_abs.txt")
except:
    pass
