# 🎫 Ticket System CLI App

A command-line ticket management system built with Python. Supports admin authentication, ticket tracking, deletion recovery (recycle bin), and password hashing.

---

## 🧩 Features

- Submit and manage tickets with persistent storage (`JSON`)
- Admin login with SHA-256 hashed passwords
- Recycle bin for deleted tickets, with timestamp and audit logging
- Change admin password securely
- Restore deleted tickets
- Data files auto-created if missing
- Uses `getpass` for hidden password input
- CLI-friendly and `.exe` exportable using PyInstaller

---

## 🔐 Admin Setup

Admin accounts are stored in `config.json` using SHA-256 password hashes.

### Admin Account Details

| Username | Password | Hashed Password |
|----------|----------|-----------------|
| admin1   | admin123 | `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9` |
| admin2   | admin234 | `9924801e8aca687d0a71f4ab14a8ed1644d48348dce8941b6cfdf7fb3076bae2` |

---

## 🔧 Generate Your Own Hashed Password

Run the following Python code:

```python
import hashlib
print(hashlib.sha256("yourpassword".encode()).hexdigest())
n
💡 Replace "yourpassword" with a password of your choice.

## ▶️ How to Run the Program

### Option 1: Run the `.exe` File (Recommended for Windows Users)

1. Download all the files in the repository.
2. Open File Explorer and navigate to the folder where you saved the files.
3. Run the `ticket.exe` program.

### Option 2: Manual Run in Terminal

1. Download all project files (including `ticket.py` and `config.json`).
2. Open your terminal or command prompt.
3. Navigate to the project folder.
4. Run the program:

```bash
python ticket.py
