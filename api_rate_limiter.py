from datetime import datetime, timedelta
import uuid

users = {}
requests = []

RATE_LIMIT = 100
TIME_WINDOW = timedelta(hours=1)


def generate_api_key():
    return "API-" + uuid.uuid4().hex[:12].upper()


def register_user():
    user_id = input("Enter User ID: ").strip()

    if not user_id:
        print("Error: User ID cannot be empty.")
        return

    if user_id in users:
        print("Error: Duplicate User ID.")
        return

    user_name = input("Enter User Name: ").strip()

    if not user_name:
        print("Error: User Name cannot be empty.")
        return

    api_key = generate_api_key()

    users[user_id] = {
        "user_name": user_name,
        "api_key": api_key,
        "status": "Active"
    }

    print("\nUser Registered Successfully!")
    print("User ID:", user_id)
    print("User Name:", user_name)
    print("API Key:", api_key)
    print("Status: Active")


def record_request():
    print("\n========== RECORD API REQUEST ==========")

    user_id = input("Enter User ID: ").strip()

    if not user_id:
        print("Error: User ID cannot be empty.")
        return

    if user_id not in users:
        print("Error: User not found.")
        return

    if users[user_id]["status"] != "Active":
        print("Error: User is not Active.")
        return

    api_key = input("Enter API Key: ").strip()

    if not api_key:
        print("Error: API Key cannot be empty.")
        return

    if api_key != users[user_id]["api_key"]:
        print("Error: Invalid API Key.")
        return

    endpoint = input("Enter API Endpoint: ").strip()

    if not endpoint:
        print("Error: API Endpoint cannot be empty.")
        return

    timestamp_input = input(
        "Enter Timestamp (YYYY-MM-DD HH:MM:SS), "
        "or press Enter for current time: "
    ).strip()

    try:
        if timestamp_input:
            timestamp = datetime.strptime(
                timestamp_input,
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            timestamp = datetime.now()

    except ValueError:
        print("Error: Invalid timestamp.")
        return

    window_start = timestamp - TIME_WINDOW

    recent_requests = [
        request for request in requests
        if request["user_id"] == user_id
        and window_start < request["timestamp"] <= timestamp
    ]

    if len(recent_requests) < RATE_LIMIT:
        request_status = "Allowed"
    else:
        request_status = "Blocked"

    request_id = len(requests) + 1

    request_data = {
        "request_id": request_id,
        "user_id": user_id,
        "endpoint": endpoint,
        "timestamp": timestamp,
        "status": request_status
    }

    requests.append(request_data)

    print("\nRequest Recorded Successfully!")
    print("Request ID:", request_id)
    print("User ID:", user_id)
    print("Endpoint:", endpoint)
    print("Timestamp:", timestamp)
    print("Request Status:", request_status)

def display_request_history():
    print("\n========== REQUEST HISTORY ==========")

    if not requests:
        print("No requests found.")
        return

    for request in requests:
        print("--------------------------------")
        print("Request ID:", request["request_id"])
        print("User ID:", request["user_id"])
        print("API Endpoint:", request["endpoint"])
        print("Timestamp:", request["timestamp"])
        print("Status:", request["status"])



# Generate API usage statistics
def generate_usage_statistics():
    print("\n========== API USAGE STATISTICS ==========")

    if not requests:
        print("No API requests found.")
        return

    total_requests = len(requests)
    allowed_requests = sum(
        1 for request in requests
        if request["status"] == "Allowed"
    )
    blocked_requests = sum(
        1 for request in requests
        if request["status"] == "Blocked"
    )

    print("Total Requests:", total_requests)
    print("Allowed Requests:", allowed_requests)
    print("Blocked Requests:", blocked_requests)

    usage_percentage = (total_requests / RATE_LIMIT) * 100

    print("Rate Limit:", RATE_LIMIT, "requests per hour")
    print("Current Usage:", f"{usage_percentage:.2f}%")

    print("\nRequests Per User:")

    for user_id, user_data in users.items():
        user_requests = [
            request for request in requests
            if request["user_id"] == user_id
        ]

        print("--------------------------------")
        print("User ID:", user_id)
        print("User Name:", user_data["user_name"])
        print("Total Requests:", len(user_requests))
        print("Allowed:", sum(
            1 for request in user_requests
            if request["status"] == "Allowed"
        ))
        print("Blocked:", sum(
            1 for request in user_requests
            if request["status"] == "Blocked"
        ))

# Change user status
def change_user_status():
    print("\n========== CHANGE USER STATUS ==========")

    user_id = input("Enter User ID: ").strip()

    if not user_id:
        print("Error: User ID cannot be empty.")
        return

    if user_id not in users:
        print("Error: User not found.")
        return

    print("1. Active")
    print("2. Blocked")

    choice = input("Select new status: ").strip()

    if choice == "1":
        users[user_id]["status"] = "Active"
    elif choice == "2":
        users[user_id]["status"] = "Blocked"
    else:
        print("Invalid status choice.")
        return

    print("User status updated successfully!")
    print("User ID:", user_id)
    print("Status:", users[user_id]["status"])
def main():
    while True:
        print("\n==============================")
        print("   API RATE LIMITER SIMULATOR")
        print("==============================")
        print("1. Register New User")
        print("2. Record API Request")
        print("3. Display Request History")
        print("4. Search Requests")
        print("5. Generate API Usage Statistics")
        print("6. Change User Status")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            record_request()

        elif choice == "3":
            display_request_history()

        elif choice == "4":
            search_requests()

        elif choice == "5":
            generate_usage_statistics()

        elif choice == "6":
            change_user_status()

        elif choice == "7":
            print("Thank you for using API Rate Limiter!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


main()

