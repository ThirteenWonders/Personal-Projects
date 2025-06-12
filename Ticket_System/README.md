# 🎫 Helpdesk Ticketing System (Python + Streamlit + Firebase)

A web-based real-time ticket management system built using Python and Streamlit, with Firebase Realtime Database for persistent storage. Designed to simulate real-world support workflows with both user and admin functionalities.

---

## 📘 Instructions

### 👤 For Users (Non-Admin)
- **Submit a Ticket**
  - Enter your name and describe your issue.
  - Click **Submit Ticket** to receive a unique Ticket ID.
  - Your ticket will be reviewed and updated by an administrator.

### 🔐 For Admins

#### Login
- Click the **Admin Login** button at the top right.
- Enter your admin username and password:
  - **Username:** `admin1`
  - **Password:** `admin123`
- Upon successful login, you’ll see additional admin functions.

#### Admin Features
- **View Tickets**: Browse all submitted tickets with status and timestamps.
- **Update Ticket**: Modify the status and add internal notes to any ticket.
- **Delete Ticket**: Soft-delete tickets (moved to a recycle bin with audit logs).
- **Restore Ticket**: Recover deleted tickets from the recycle bin.

---

## 💡 Notes

- Data is saved in **Firebase Realtime Database** and persists across sessions.
- Admin passwords are securely hashed using **SHA-256**.
- Admin actions like deletions are logged for transparency and accountability.

---

## 🚀 Live App
[Streamlit App](https://appticketingsystem.streamlit.app/)

---

## 📩 Support
For assistance, please contact the system administrator at **nicholasang1@outlook.com**
