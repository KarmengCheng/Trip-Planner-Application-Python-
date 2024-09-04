import os
import json

DATABASE_FILE = 'database.json'
logged_in_merchant = None

# Load data from the JSON file
def load_data():
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("users", {}), data.get("services", {}), data.get("bookings", {})
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return {}, {}, {}
    return {}, {}, {}

# Save data to the JSON file
def save_data(users, services, bookings):
    try:
        with open(DATABASE_FILE, 'w') as f:
            json.dump({
                "users": users,
                "services": services,
                "bookings": bookings,
                "triprecommendations": {}  # Preserve the original structure
            }, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# Merchant login function
def login(users):
    global logged_in_merchant
    username = input("Enter your merchant username: ")
    password = input("Enter your password: ")

    if username in users and users[username]['role'] == 'merchant' and users[username]['password'] == password:
        if users[username]["status"].upper() == "ACTIVE":
            logged_in_merchant = username
            print("Login successful!")
            return True
        else:
            print("Your account is blocked.")
            return False
    else:
        print("Invalid username or password.")
        return False

# Merchant logout function
def logout():
    global logged_in_merchant
    logged_in_merchant = None
    print("You have been logged out.")

# View all services provided by the logged-in merchant
def view_own_services(services):
    if services:
        print("Your services:")
        for service_id, service_info in services.items():
            if service_info['merchant_name'] == logged_in_merchant:
                print(f"Service ID: {service_id}")
                print(f"Name: {service_info['name']}")
                print(f"Description: {service_info['description']}")
                print(f"Price: {service_info['price']}")
                print(f"Dates: {', '.join(service_info['dates'])}")
                print(f"Max Customers: {service_info['max_customers']}")
                print(f"Current Customers: {service_info['current_customers']}")
                if 'hotel_name' in service_info:
                    print(f"Hotel: {service_info['hotel_name']}")
                if 'notable_restaurants' in service_info:
                    print(f"Notable Restaurants: {', '.join(service_info['notable_restaurants'])}")
                if 'duration' in service_info:
                    print(f"Duration: {service_info['duration']} day(s)")
                print("-----------------------------------")
    else:
        print("No services listed.")

# Add a new service
def add_service(users, services):
    if not logged_in_merchant:
        print("You need to be logged in to add a service.")
        return

    service_id = str(len(services) + 1)
    merchant_id = users[logged_in_merchant]['id']
    merchant_name = logged_in_merchant
    name = input("Enter the service name: ")
    description = input("Enter the service description: ")
    price = input("Enter the service price: ")
    dates = input("Enter the available dates (comma separated): ").split(',')
    max_customers = int(input("Enter the maximum number of customers: "))
    current_customers = 0
    hotel_name = input("Enter the hotel name (if any): ")
    notable_restaurants = input("Enter the notable restaurants (comma separated): ").split(',')
    duration = int(input("Enter the service duration (in days): "))

    services[service_id] = {
        "merchant_id": merchant_id,
        "merchant_name": merchant_name,
        "name": name,
        "description": description,
        "price": price,
        "dates": dates,
        "max_customers": max_customers,
        "current_customers": current_customers,
        "hotel_name": hotel_name,
        "notable_restaurants": notable_restaurants,
        "duration": duration
    }

    save_data(users, services, bookings)
    print("Service added successfully.")

# Update an existing service
def update_service(users, services):
    if not logged_in_merchant:
        print("You need to be logged in to update a service.")
        return

    service_id = input("Enter the service ID to update: ")
    if service_id not in services:
        print("Service not found.")
        return

    service = services[service_id]
    if service['merchant_name'] != logged_in_merchant:
        print("You can only update your own services.")
        return

    print("Leave blank to keep the current value.")
    service['name'] = input(f"Enter the new service name ({service['name']}): ") or service['name']
    service['description'] = input(f"Enter the new service description ({service['description']}): ") or service['description']
    service['price'] = input(f"Enter the new service price ({service['price']}): ") or service['price']
    service['dates'] = input(f"Enter the new available dates (comma separated) ({', '.join(service['dates'])}): ").split(',') or service['dates']
    service['max_customers'] = int(input(f"Enter the new maximum number of customers ({service['max_customers']}): ") or service['max_customers'])
    service['hotel_name'] = input(f"Enter the new hotel name ({service['hotel_name']}): ") or service['hotel_name']
    service['notable_restaurants'] = input(f"Enter the new notable restaurants (comma separated) ({', '.join(service['notable_restaurants'])}): ").split(',') or service['notable_restaurants']
    service['duration'] = int(input(f"Enter the new service duration (in days) ({service['duration']}): ") or service['duration'])

    save_data(users, services, bookings)
    print("Service updated successfully.")

# Delete a service
def delete_service(users, services):
    if not logged_in_merchant:
        print("You need to be logged in to delete a service.")
        return

    service_id = input("Enter the service ID to delete: ")
    if service_id not in services:
        print("Service not found.")
        return

    if services[service_id]['merchant_name'] != logged_in_merchant:
        print("You can only delete your own services.")
        return

    del services[service_id]
    save_data(users, services, bookings)
    print("Service deleted successfully.")

# View, cancel, and confirm bookings
def manage_bookings(bookings, services):
    if not logged_in_merchant:
        print("You need to be logged in to manage bookings.")
        return

    print("Your Bookings:")
    for user, user_bookings in bookings.items():
        for booking in user_bookings:
            service_id = booking['option']
            if service_id in services and services[service_id]['merchant_name'] == logged_in_merchant:
                print(f"User: {user}")
                print(f"Service ID: {service_id}")
                print(f"Service Name: {services[service_id]['name']}")
                print(f"Dates: {', '.join(booking['dates'])}")
                print(f"Pax: {booking['pax']}")
                print(f"Duration: {booking['duration']}")
                print(f"Total: {booking['total']}")
                print("-----------------------------------")

    action = input("Do you want to cancel or confirm a booking? (cancel/confirm): ").lower()
    if action not in ['cancel', 'confirm']:
        print("Invalid action.")
        return

    user = input("Enter the username of the booking: ")
    service_id = input("Enter the service ID of the booking: ")

    if user not in bookings or not any(b['option'] == service_id for b in bookings[user]):
        print("Booking not found.")
        return

    if action == 'cancel':
        bookings[user] = [b for b in bookings[user] if b['option'] != service_id]
        save_data(users, services, bookings)
        print("Booking canceled successfully.")
    elif action == 'confirm':
        print("Booking confirmed.")  # Here you can add additional logic for confirming bookings

# Main menu and greetings
def mainmenu():
    print(
        "Welcome to the Merchant Management System\n"
        "1. Login\n"
        "2. Logout/Exit\n"
        "3. View Your Services\n"
        "4. Add a New Service\n"
        "5. Update an Existing Service\n"
        "6. Delete a Service\n"
        "7. Manage Bookings\n"
        "8. Exit")

# Load initial data
users, services, bookings = load_data()

# Main loop to keep the app running
def merchantloop():
    while True:
        mainmenu()
        choice = input("\nYour choice: ")
        if choice == "1":
            if not logged_in_merchant:
                login(users)
            else:
                print("You are already logged in.")
        elif choice == "2":
            if logged_in_merchant:
                logout()
            exit_choice = input("Are you sure you want to exit? (yes/no): ").lower()
            if exit_choice == "yes":
                print("Thanks for using the Merchant Management System")
                break  # Exit the application
        elif choice == "3":
            view_own_services(services)
        elif choice == "4":
            add_service(users, services)
        elif choice == "5":
            update_service(users, services)
        elif choice == "6":
            delete_service(users, services)
        elif choice == "7":
            manage_bookings(bookings, services)
        elif choice == "8":
            exit_choice = input("Are you sure you want to exit? (yes/no): ").lower()
            if exit_choice == "yes":
                print("Thanks for using the Merchant Management System")
                break  # Exit the application
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    merchantloop()