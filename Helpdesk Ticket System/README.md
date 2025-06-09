# 🎫 Ticket System CLI App

A command-line ticket management system built with Python. Supports admin authentication, ticket tracking, deletion recovery (recycle bin), and password hashing.


## 🧩 Features

- Submit and manage tickets with persistent storage (`JSON`)
- Admin login with SHA-256 hashed passwords
- Recycle bin for deleted tickets, with timestamp and audit logging
- Change admin password securely
- Restore deleted tickets
- Data files auto-created if missing
- CLI-friendly and `.exe` exportable using PyInstaller

---

## 🔐 Admin Setup


Admin accounts are stored in `config.json` using SHA-256 password hashes.  

## Admin account details
Username: admin1
Password: admin123

Username: admin2
Password: admin234

Password hashes for both accounts
admin1: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
admin2: 9924801e8aca687d0a71f4ab14a8ed1644d48348dce8941b6cfdf7fb3076bae2

## To generate your own hashed password
in python run the following code,

import hashlib
print(hashlib.sha256("yourpassword".encode()).hexdigest())

## Note: replace "yourpassword" with a password of your choice
------------------------------------------

## How to run program?
Option 1: Download all files
