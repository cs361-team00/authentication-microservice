# authentication-microservice

Authentication microservice for user registration, login, and secure password resets. Uses SQLite for persistence and Flask-Bcrypt for secure password hashing.

## Run locally

1. **Create a virtualenv and install dependencies:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate   # On Windows PowerShell
   python -m pip install -r requirements.txt

2. **Start the server**
   ```powershell
   python auth_service.py
  Server listens on http://localhost:5000
