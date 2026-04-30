import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print("-" * 30)

def test_flow():
    print("--- STARTING API TEST ---")

    # 1. TEST REGISTRATION
    print("\n1. Testing Registration...")
    reg_data = {"user_email": "tester@example.com", "user_pass": "SecurePass123"}
    r_reg = requests.post(f"{BASE_URL}/register", json=reg_data)
    print_response(r_reg)

    # 2. TEST LOGIN
    print("\n2. Testing Login...")
    login_data = {"user_email": "tester@example.com", "user_pass": "SecurePass123"}
    r_login = requests.post(f"{BASE_URL}/login", json=login_data)
    print_response(r_login)

    # 3. TEST PASSWORD RESET REQUEST
    print("\n3. Testing Password Reset Request...")
    r_reset_req = requests.post(f"{BASE_URL}/request-reset", json={"user_email": "tester@example.com"})
    res_data = r_reset_req.json()
    print_response(r_reset_req)

    # 4. TEST PASSWORD RESET EXECUTION
    if r_reset_req.status_code == 200:
        token = res_data.get('reset_token')
        print(f"\n4. Testing Reset with Token: {token}")
        reset_exec_data = {
            "reset_token": token,
            "new_password": "NewStrongPassword789"
        }
        r_final = requests.post(f"{BASE_URL}/reset-password", json=reset_exec_data)
        print_response(r_final)

        # 5. VERIFY NEW LOGIN
        print("\n5. Verifying Login with NEW password...")
        verify_data = {"user_email": "tester@example.com", "user_pass": "NewStrongPassword789"}
        r_verify = requests.post(f"{BASE_URL}/login", json=verify_data)
        print_response(r_verify)

if __name__ == "__main__":
    try:
        test_flow()
    except requests.exceptions.ConnectionError:
        print("ERROR")
