# authentication-microservice

Authentication microservice for user registration, login, and secure password resets. Uses SQLite for persistence and Flask-Bcrypt for secure password hashing.

## How to run

1. **Create a virtualenv and install dependencies:**
   ```powershell
   # Open file in VSCode and open a new terminal (PowerShell)
   python -m venv venv
   .\venv\Scripts\activate   # On Windows PowerShell
   python -m pip install flask flask-bcrypt requests

3. **Start the server**
   ```powershell
   python auth_service.py
   # Server listens on http://localhost:5000

4. **Test API:**
   ```powershell
   # Open new terminal and run:
   python test_api.py

## How to request and receive data
To request data, the calling program must send an HTTP POST request to the desired endpoint with a JSON-formatted body.
<br><br>
**Example Call (Python):**
Request to register a new user with a username and a password
```python
import requests

# The request payload
request_payload = {"user_email": "user@example.com", "user_pass": "SecurePass123"}

# Sending the programmatic request
response = requests.post("http://localhost:5000/api/register", json=request_payload)
