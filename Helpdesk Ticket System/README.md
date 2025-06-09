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
</br>
Username: admin1
</br>
Password: admin123
</br>
</br>
Username: admin2
</br>
Password: admin234
</br>
</br>
Password hashes for both accounts
</br>
</br>
admin1: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
</br>
admin2: 9924801e8aca687d0a71f4ab14a8ed1644d48348dce8941b6cfdf7fb3076bae2

---

## To generate your own hashed password
in python run the following code,

import hashlib
</br>
print(hashlib.sha256("yourpassword".encode()).hexdigest())

## Note: replace "yourpassword" with a password of your choice
------------------------------------------

## How to run program?
</br>
Option 1: Manual run in terminal
</br>
</br>
1. Download all the files
</br>
</br>
2. Navigate to the folder with all the files downloaded
</br>
</br>
3. Run the following in terminal (Command Prompt / PowerShell):
</br>
</br>
python ticket.py
</br>

Option 2: Run the ticket system program
</br>
1. Download all the files in the repository
   </br>
   </br>
3. In file explorer, navigate to the folder where you downloaded the files
 </br>
   </br>
5. Run the "ticket.exe" program


