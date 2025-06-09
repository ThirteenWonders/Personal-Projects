import json
import os
from datetime import datetime
import shutil
from getpass import getpass
import hashlib

# Ticket structure
tickets = []
ticket_counter = 1  # start counting from 1

# Store tickets in a file
TICKETS_FILE = "tickets.json"
COUNTER_FILE =  "counters.json"
RECYCLE_BIN_FILE = "deleted_tickets.json"



def load_data():
    global tickets, ticket_counter
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            tickets = json.load(f)
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            ticket_counter = int(f.read())

def load_deleted_tickets():
    if os.path.exists(RECYCLE_BIN_FILE):
        with open(RECYCLE_BIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_deleted_ticket(ticket):
    deleted = load_deleted_tickets()
    deleted.append(ticket)
    with open(RECYCLE_BIN_FILE, "w") as f:
        json.dump(deleted, f, indent=2)

def save_data():
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(ticket_counter))


def create_ticket():
    global ticket_counter
    ticket_id = f"TICKET-{ticket_counter:03d}"  # e.g., TICKET-001
    user = input("Enter your name: ")
    issue = input("Describe your issue: ")
    ticket = {
        "id": ticket_id,
        "user": user,
        "issue": issue,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "notes": [] # Empty list as user does not need to input

    }
    tickets.append(ticket)
    ticket_counter += 1
    save_data()
    print(f"\n Hi {user}, we have received your support request and will be reviewing it shortly. We aim to respond as soon as possible.")
    print(f"\n Your Ticket ID is: {ticket_id}\n")


def view_tickets():
    if not tickets:
        print("\nNo tickets found.\n")
        return

    print("\n========== TICKETS ==========\n")
    for ticket in tickets:
        print(f"Ticket ID   : {ticket['id']}")
        print(f"User        : {ticket['user']}")
        print(f"Issue       : {ticket['issue']}")
        print(f"Status      : {ticket['status']}")
        print(f"Created At  : {ticket.get('created_at', 'N/A')}")

        # Display notes, if any
        if ticket.get("notes"):
            print("Notes:")
            for i, note in enumerate(ticket["notes"], 1):
                if isinstance(note, dict):  # timestamped note
                    print(f"  {i}. [{note['timestamp']}] {note['text']}")
                else:  # old style plain string note
                    print(f"  {i}. {note}")
        else:
            print("Notes       : None")

        print("-" * 30)


def update_ticket():
    view_tickets()
    ticket_id = input("Enter Ticket ID to update: ").strip().upper()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            valid_statuses = ["Open", "In Progress", "Closed"]

            while True:
                new_status = input("Enter new status (Open/In Progress/Closed): ").strip().title()
                if new_status in valid_statuses:
                    ticket["status"] = new_status
                    break
                else:
                    print("Invalid status. Please enter one of: Open, In Progress, Closed.\n")

            note_text = input("Add a note describing the update: ")
            note_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "text": note_text
            }
            ticket["notes"].append(note_entry)
            save_data()
            print("Ticket updated with new status and note.\n")
            return
    print("Ticket not found.\n")

def delete_ticket(admin_username):
    if not tickets:
        print("\nNo tickets to delete.\n")
        return

    print("\n=== Delete Ticket ===")
    print("Available Tickets:")
    for ticket in tickets:
        issue_preview = ticket['issue'][:30] + "..." if len(ticket['issue']) > 30 else ticket['issue']
        print(f"  - {ticket['id']} | Status: {ticket['status']} | User: {ticket['user']} | Issue: {issue_preview}")

    ticket_id = input("Enter Ticket ID to delete: ").strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            # Display ticket info before confirming
            print(f"\nTicket ID   : {ticket['id']}")
            print(f"User        : {ticket['user']}")
            print(f"Issue       : {ticket['issue']}")
            print(f"Status      : {ticket['status']}")
            confirm = input("Are you sure you want to delete this ticket? (y/n): ").strip().lower()

            if confirm == 'y':
                # log to recycle bin with admin who deleted
                deleted_entry = ticket.copy()
                deleted_entry['deleted_by'] = admin_username
                deleted_entry['deleted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_deleted_ticket(deleted_entry)

                tickets.remove(ticket)
                save_data()
                print("Ticket deleted and moved to recycle bin.\n")
            else:
                print("Deletion cancelled.\n")
            return

    print("Invalid Ticket ID. No ticket deleted.\n")

def restore_deleted_ticket():
    deleted = load_deleted_tickets()
    if not deleted:
        print("\nRecycle bin is empty.\n")
        return

    print("\n=== Deleted Tickets (Recycle Bin) ===")
    for i, ticket in enumerate(deleted, 1):
        print(f"{i}. ID: {ticket['id']} | User: {ticket['user']} | Status: {ticket['status']} | "
              f"Deleted by: {ticket.get('deleted_by', 'Unknown')} at {ticket.get('deleted_at', 'Unknown')}")

    try:
        choice = int(input("Enter the number of the ticket to restore: ")) - 1
        if 0 <= choice < len(deleted):
            restored_ticket = deleted.pop(choice)
            # Remove tracking fields before restoring
            restored_ticket.pop('deleted_by', None)
            restored_ticket.pop('deleted_at', None)

            tickets.append(restored_ticket)
            save_data()

            with open(RECYCLE_BIN_FILE, "w") as f:
                json.dump(deleted, f, indent=2)

            print("Ticket restored successfully.\n")
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")


# Allows administrators to track individual ticket history
def search_by_user():
    name = input("Enter name to search: ")
    for ticket in tickets:
        if ticket["user"].lower() == name.lower():
            print(f"ID: {ticket['id']}, Issue: {ticket['issue']}, Status: {ticket['status']}")

def backup_data():
    shutil.copy(TICKETS_FILE, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def load_admins_hash():
    try:
        with open("config.json") as f:
            config = json.load(f)
        return config.get("admins", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load admin credentials.")
        return {}


def admin_login():
    admins = load_admins_hash()
    if not admins:
        return None  # no login
    # Set attempt limits to 3
    for attempt in range(3):
        username = input("Enter admin username: ").strip()
        if username not in admins:
            print("Invalid username.\n")
            continue

        password = getpass("Enter admin password: ")
        hashed = hashlib.sha256(password.encode()).hexdigest()

        # Compare hashed user input against hashed password in json file
        if hashed == admins[username]:
            print(f"\nAccess granted. \n\nWelcome, {username}!\n")
            return username  # return the logged-in admin
        else:
            print(f"Incorrect password. {2 - attempt} attempts left.\n")

    print("Too many failed attempts. Returning to main menu.\n")
    return None

# Function to change admin password
def change_admin_password(username):
    admins = load_admins_hash()
    if username not in admins:
        print("Admin username not found.\n")
        return

    print(f"\n=== Change Password for {username} ===")

    # Step 1: Authenticate current password
    current_password = getpass("Enter current password: ")
    current_hash = hashlib.sha256(current_password.encode()).hexdigest()

    if current_hash != admins[username]:
        print("Incorrect current password. Password not changed.\n")
        return

    # Step 2: Ask for new password twice
    new_password = getpass("Enter new password: ")
    confirm_password = getpass("Confirm new password: ")

    if new_password != confirm_password:
        print("Passwords do not match. Password not changed.\n")
        return

    # Step 3: Save updated hash back to config
    new_hash = hashlib.sha256(new_password.encode()).hexdigest()
    admins[username] = new_hash

    try:
        with open("config.json", "w") as f:
            json.dump({"admins": admins}, f, indent=2)
        print("Password updated successfully for", username)
    except Exception as e:
        print("Failed to update password:", e)




# Let the administrators view tickets by status
def filter_tickets():
    status = input("Enter status to filter by (Open/In Progress/Closed): ")
    for ticket in tickets:
        if ticket["status"].lower() == status.lower():
            print(f"ID: {ticket['id']}, User: {ticket['user']}, Issue: {ticket['issue']}, Status: {ticket['status']}")

def admin_menu():
    username = admin_login()
    if not username:
        return

    while True:
        print("\n====== ADMIN MENU ======")
        print("1. View All Tickets")
        print("2. Update Ticket Status")
        print("3. Filter Tickets by Status")
        print("4. Search Tickets by User")
        print("5. Delete a Ticket")
        print("6. Restore Deleted Ticket")
        print("7. Change Admin Password")
        print("8. Return to Main Menu")
        print("========================")

        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            view_tickets()
        elif choice == '2':
            update_ticket()
        elif choice == '3':
            filter_tickets()
        elif choice == '4':
            search_by_user()
        elif choice == '5':
            delete_ticket(username)
        elif choice == '6':
            restore_deleted_ticket()
        elif choice == '7':
            change_admin_password(username)
        elif choice == '8':
            print("Returning to main menu...\n")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 8.")




def menu():
    while True:
        print("\n========= TICKET SYSTEM =========")
        print("1. Submit New Ticket")
        print("2. Admin Menu (Restricted)")
        print("3. Exit")
        print("=================================")

        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            create_ticket()
        elif choice == '2':
            admin_menu()
        elif choice == '3':
            print("Exiting... Goodbye!\n")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 3.")


# Start the system
load_data()
menu()
