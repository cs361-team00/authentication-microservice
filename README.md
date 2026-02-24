# authentication-microservice

Authentication microservice for user registration, login, and secure password resets. Uses SQLite for persistence and Flask-Bcrypt for secure password hashing.

## Run locally

1. **Create a virtualenv and install dependencies:**
   *Open file in VSCode and open a new terminal (PowerShell)*
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate   # On Windows PowerShell
   python -m pip install flask flask-bcrypt requests

3. **Start the server:**
   *Open another terminal and execute the program*
   ```powershell
   python auth_service.py
  Server listens on http://localhost:5000
