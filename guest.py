import os
import json
import traveller
import merchant
DATABASE_FILE = 'database.json'

# Load data from the JSON file
def load_data():
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("users", {}), data.get("services", {}), data.get("triprecommendations", {})
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return {}, {}, {}
    return {}, {}, {}

# Save data to the JSON file
def save_data(users, services, trip_recommendations):
    try:
        with open(DATABASE_FILE, 'w') as f:
            json.dump({
                "users": users,
                "services": services,
                "triprecommendations": trip_recommendations
            }, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# View all services provided by merchants
def view_all_services(services):
    if services:
        print("All services:")
        for service_id, service_info in services.items():
            print(f"Service ID: {service_id}")
            print(f"Merchant: {service_info['merchant_name']}")
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

# Search for services based on user input
def search_service(services):
    search_term = input("Enter a keyword to search for services: ").strip().lower()
    found_services = []

    for service_id, service_info in services.items():
        if (search_term in service_info['name'].lower() or
                search_term in service_info['description'].lower()):
            found_services.append((service_id, service_info))

    if found_services:
        print(f"Found {len(found_services)} service(s) matching '{search_term}':")
        for service_id, service_info in found_services:
            print(f"Service ID: {service_id}")
            print(f"Merchant: {service_info['merchant_name']}")
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
        print(f"No services found matching '{search_term}'.")

# Display trip recommendations
def view_trip_recommendations(trip_recommendations):
    if trip_recommendations:
        destinations = trip_recommendations.get("destinations", [])
        promotions = trip_recommendations.get("promotions", [])

        print("Trip Recommendations:\n")

        print("Destinations:")
        for destination in destinations:
            print(f"Name: {destination['name']}")
            print(f"Description: {destination['description']}")
            print(f"Attractions: {', '.join(destination['attractions'])}")
            print("-----------------------------------")

        print("Promotions:")
        for promo in promotions:
            print(f"Promo Code: {promo['promo_code']}")
            print(f"Title: {promo['title']}")
            print(f"Description: {promo['description']}")
            print(f"Discount: {promo['discount']}")
            print(f"Valid Month: {promo['valid_month']}")
            print("-----------------------------------")
    else:
        print("No trip recommendations available.")

# Find the next available merchant id without using max
def find_next_merchant_id(users):
    next_merchant_id = 0
    for user in users.values():
        if user['role'] == 'merchant' and user['id'] > next_merchant_id:
            next_merchant_id = user['id']
    return next_merchant_id + 1

# Main menu and greetings
def mainmenu():
    print(
        "Welcome to the Trip Planner Application, you are browsing as a guest\n"
        "1. View All Services\n"
        "2. Search Services\n"
        "3. View recommended itineraries\n"
        "4. Sign Up for an account\n"
        "5. Login\n"
        "6. Exit")

def signup(users, services, trip_recommendations):
    while True:
        print("\nDo you want to \n1. Sign up as a Traveller \n2. Sign up as a Merchant \n3. Back")
        choice2 = input("\nYour choice: ")
        if choice2 == "1":
            print("Signing up as a traveller ")
            signup_process("traveller", users, services, trip_recommendations)
            break
        elif choice2 == "2":
            print("Signing up as a merchant ")
            signup_process("merchant", users, services, trip_recommendations)
            break
        elif choice2 == "3":
            return
        else:
            print("Invalid option, please try again")

def signup_process(role, users, services, trip_recommendations):
    while True:
        username = input("Enter username (or type 'esc' to go back): ")
        if username.lower() == 'esc':
            return  # Exit the function to go back to the previous menu
        if len(username) < 5:
            print("The username must be at least 5 characters long, please try again")
        elif ' ' in username:
            print("The username cannot contain spaces, please try again")
        elif username in users:
            print("The username is taken, please try again")
        else:
            while True:
                password1 = input("Enter password (or type 'back' to edit username, 'esc' to go back to main menu): ")
                if password1.lower() == 'esc':
                    return  # Exit the function to go back to the main menu
                elif password1.lower() == 'back':
                    break  # Break the password loop to edit username
                if len(password1) < 8:
                    print("The password must be at least 8 characters long, please try again")
                    continue
                elif ' ' in password1:
                    print("The password cannot contain spaces, please try again")
                    continue
                while True:
                    password2 = input("Re-enter password (or type 'back' to edit password, 'esc' to go back to main menu): ")
                    if password2.lower() == 'esc':
                        return  # Exit the function to go back to the main menu
                    elif password2.lower() == 'back':
                        break  # Break the inner loop to re-enter the first password
                    if password1 == password2:
                        if role == 'merchant':
                            # Find the next available merchant id
                            next_merchant_id = find_next_merchant_id(users)
                            users[username] = {
                                "password": password1,
                                "role": role,
                                "id": next_merchant_id
                            }
                        else:  # For traveller
                            users[username] = {
                                "password": password1,
                                "role": role,
                                "profile": ""
                            }
                        save_data(users, services, trip_recommendations)
                        print("Account created successfully!")
                        return  # Exit the function after account creation
                    else:
                        print("The passwords do not match, please try again")
                if password2.lower() == 'back':
                    continue  # Continue the outer loop to re-enter the first password
            if password1.lower() == 'back':
                continue  # Continue the outer loop to edit the username


def login(users, services, trip_recommendations):
    while True:
        print("\nDo you want to \n1. Login as a Traveller \n2. Login as a Merchant \n3. Back")
        choice2 = input("\nYour choice: ")
        if choice2 == "1":
            traveller.travellerloop()
        elif choice2 == "2":
            merchant.merchantloop()
        elif choice2 == "3":
            return
        else:
            print("Invalid option, please try again")

# Load initial data
users, services, trip_recommendations = load_data()

# Main loop to keep the app running
def guestloop():
    while True:
        mainmenu()
        choice1 = input("\nYour choice: ")
        if choice1 == "1":
            view_all_services(services)
        elif choice1 == "2":
            search_service(services)
        elif choice1 == "3":
            view_trip_recommendations(trip_recommendations)
        elif choice1 == "4":
            signup(users, services, trip_recommendations)
        elif choice1 == "5":
            login(users, services, trip_recommendations)
        elif choice1 == "6":
            exit_choice = input("Are you sure you want to exit? (yes/no): ").lower()
            if exit_choice == "yes":
                break
        else:
            print("Invalid choice, please try again.")

# Final save before exiting
save_data(users, services, trip_recommendations)

if __name__ == "__main__":
    guestloop()