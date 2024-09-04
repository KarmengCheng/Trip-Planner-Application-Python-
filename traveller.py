import os
import json

from datetime import datetime

DATABASE_FILE = 'database.json'

#load data from json file
def load_data():
    users = {}
    bookings = {}
    services = {}
    promotions = {}

    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'r') as f:
                data = f.read().strip()
                if data:
                    file_data = json.loads(data)
                    users = file_data.get("users", {})
                    bookings = file_data.get("bookings", {})
                    services = file_data.get("services", {})
                    promotions = {promo["promo_code"]: promo for promo in file_data.get("triprecommendations", {}).get("promotions", [])}
                else:
                    print("Database file is empty.")
        except json.JSONDecodeError:
            print("Error: The JSON file is not valid.")
            exit(1)
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            exit(1)
    else:
        print("Database file not found.")
        exit(1)

    return users, bookings, services, promotions

# save data to json file
def save_data(users, bookings, services, promotions):
    try:
        with open(DATABASE_FILE, 'w') as f:
            data = {
                "users": users,
                "bookings": bookings,
                "services": services,
                "triprecommendations": {
                    "promotions": list(promotions.values())
                }
            }
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

# Traveller to login
def login(users):
    username = input("Enter username: ")
    password = input("Enter password: ")

    if len(password) == 0:
        print("Please enter your password.")
        return None

    if username in users and password == users[username]["password"]:
        if users[username]["status"].upper() == "ACTIVE":
            if users[username]["role"].lower() == "traveller":
                print(f"Login successful! Welcome, {username}")
                return username
            else:
                print("Only Travellers are allowed to log in.")
                return None
        else:
            print("Your account is blocked.")
            return None
    else:
        print("Invalid username or password")
        return None

# for user to make changes of their profile
def update_profile(logged_in_user, users, bookings, services,promotions):
    if logged_in_user:
        print("\nUpdate Profile Options:")
        print("1. Change Password")
        print("2. Update Personal Information")
        print("3. Change Username")
        choice = input("Your choice: ")

        if choice == "1":
            old_password = input("Enter old password (leave blank to keep current password): ")
            if old_password == users[logged_in_user]["password"]:
                new_password1 = input("Enter new password (leave blank to keep current password): ")
                new_password2 = input("Re-enter new password (leave blank to keep current password): ")
                if new_password1 == new_password2:
                    if new_password1 != "":
                        users[logged_in_user]["password"] = new_password1
                        print("Password updated successfully.")
                    else:
                        print("Password is not changed.")
                else:
                    print("Passwords do not match. Try again.")
            else:
                print("Old password is incorrect.")

        elif choice == "2":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            if "@" in email and "." in email:
                users[logged_in_user]["profile"] = {"name": name, "email": email}
                save_data(users, bookings, services,promotions)
                print("Profile information updated successfully.")
            else:
                print("Invalid email format.")

        elif choice == "3":
            new_username = input("Enter your new username: ")
            if new_username in users:
                print("Username already taken, please try again.")
            else:
                users[new_username] = users.pop(logged_in_user)
                if logged_in_user in bookings:
                    bookings[new_username] = bookings.pop(logged_in_user)
                save_data(users, bookings, services,promotions)
                print("Username updated successfully.")
                return new_username
        else:
            print("Invalid option. Returning to main menu.")
    else:
        print("You need to log in first")
    return logged_in_user

# View booking information
def view_bookings_info(logged_in_user, bookings, services):
    if logged_in_user in bookings and bookings[logged_in_user]:
        print(f"Bookings for {logged_in_user}:")
        for idx, booking_info in enumerate(bookings[logged_in_user], start=1):
            booking_details = booking_info
            service_id = booking_details.get("option", 0)
            service = services.get(service_id, {"name": "Unknown", "description": "N/A", "price": 0})
            print(f"  {idx}. {service['name']} - {service['description']} - Price per person: RM {service['price']}")
            print(f"Dates: {booking_details.get('dates', 'N/A')}\n, "
                  f"Number of pax: {booking_details.get('pax', 'N/A')}\n, "
                  f"Total: RM {booking_details.get('total', 'N/A')}")
    else:
        print("No bookings available.")

# plan and book a trip
def plan_trip(logged_in_user, users, bookings, services, promotions):
    if logged_in_user:
        print("\n1. View products and services\n2. Book a product or service\n3. Search for a KL trip\n4. Cancel a booking")
        choice = input("Your choice: ")

        if choice == "1":
            display_services(services)

        elif choice == "2":
            book_service(logged_in_user, users, bookings, services, promotions)

        elif choice == "3":
            search_service(services)

        elif choice == "4":
            view_bookings_info(logged_in_user, bookings, services)
            cancel_index = input("Enter the booking number to cancel: ")
            if cancel_index.isdigit():
                cancel_index = int(cancel_index)
                if 1 <= cancel_index <= len(bookings.get(logged_in_user, [])):
                    del bookings[logged_in_user][cancel_index - 1]
                    if not bookings[logged_in_user]:
                        del bookings[logged_in_user]
                    save_data(users, bookings, services,promotions)
                    print("Booking cancelled successfully")
                else:
                    print("Invalid booking number")
            else:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice")
    else:
        print("You need to log in first")

# show users trip package available
def display_services(services):
    for service_id, service_info in services.items():
        print(
            f"ID: {service_id}\n, "
            f"Name: {service_info['name']}\n, "
            f"Description: {service_info['description']}\n, "
            f"Total Price: RM {service_info['price']}\n, "
            f"Available Dates: {service_info['dates']}\n, "
            f"Current pax: {service_info['current_customers']}\n, "
            f"Maximum pax: {service_info['max_customers']}\n, "
            f"Hotel: {service_info['hotel_name']}\n, "
            f"Notable restaurant: {service_info['notable_restaurants']}"
        )

# book trip
def book_service(logged_in_user, users, bookings, services, promotions):
    try:
        duration = int(input("Enter the trip duration in days (1, 2, or 3): "))
        if duration not in [1, 2, 3]:
            print("Invalid duration. Please enter 1, 2, or 3.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    print(f"\nServices available for a {duration}-day trip:\n")
    filtered_services = {
        service_id: info
        for service_id, info in services.items()
        if info.get('duration') == duration
    }

    if not filtered_services:
        print("No services available for the selected duration.")
        return

    display_services(filtered_services)

    while True:
        option = input("Enter product ID to book (leave blank to exit booking): ")
        if option == "":
            print("Exiting booking.")
            break

        if option in filtered_services:
            service_id = option
            service_info = filtered_services[service_id]
            try:
                service_price_str = service_info['price'].replace("RM", "").replace(",", "").strip()
                service_price = float(service_price_str)
            except ValueError:
                print("Invalid price format. Booking cancelled.")
                return

            start_date = input("Enter start date (YYYY-MM-DD) to book: ")
            if not start_date:
                print("Start date is required. Booking cancelled.")
                return

            if start_date in service_info['dates']:
                dates = [start_date]
                if duration > 1:
                    for i in range(1, duration):
                        extra_date = input(f"Enter additional date {i} (YYYY-MM-DD): ")
                        if not extra_date:
                            print("All dates are required. Booking cancelled.")
                            return
                        if extra_date in service_info['dates']:
                            dates.append(extra_date)
                        else:
                            print("Invalid date. Please choose from the available dates. Booking cancelled.")
                            return

                if len(dates) == duration:
                    pax = input("Enter number of pax: ")
                    if not pax.isdigit() or int(pax) <= 0:
                        print("Valid number of pax is required. Booking cancelled.")
                        return

                    pax = int(pax)
                    total = service_price * pax
                    print(f"Total amount for {duration} days and {pax} pax: RM {total}")

                    print(f"Loaded promotions: {promotions.keys()}")
                    promo_code = input("Enter promo code (if any) or press Enter to skip: ").strip().upper()
                    if promo_code in promotions:
                        promo_info = promotions[promo_code]
                        current_month = datetime.now().strftime("%B %Y")
                        print(f"Promo Code Entered: {promo_code}")
                        print(f"Promo Code Valid Month: {promo_info['valid_month']}")
                        print(f"Current Month: {current_month}")

                        if promo_info["valid_month"].strip() == current_month:
                            try:
                                discount_percentage = float(
                                    promo_info["discount"].replace("% off hotels booked", "").strip())
                                discount = discount_percentage / 100
                                total *= (1 - discount)
                                print(
                                    f"Promo code applied. Discount: {discount_percentage}%. New total: RM {total:.2f}")
                            except ValueError:
                                print("Invalid discount format in the promo code. No discount applied.")
                        else:
                            print(
                                f"Promo code is not valid for the current month ({current_month}). No discount applied.")
                    else:
                        if promo_code:
                            print("Invalid promo code. No discount applied.")

                    confirmation = input("Enter 1 to confirm booking (leave blank to exit booking): ")
                    if confirmation == "1":
                        if logged_in_user not in bookings:
                            bookings[logged_in_user] = []
                        bookings[logged_in_user].append({
                            "option": service_id,
                            "dates": dates,
                            "pax": pax,
                            "duration": duration,
                            "total": total
                        })

                        save_data(users, bookings, services,promotions)
                        print("Booking confirmed")
                    else:
                        print("Booking cancelled")
                else:
                    print("Booking cancelled due to missing dates.")
            else:
                print("Invalid start date. Please choose from the available dates. Booking cancelled.")
        else:
            print("Invalid option. Please enter a valid service ID. Booking cancelled.")

# search places available in the trip package
def search_service(services):
    while True:
        search_term = input("Enter a keyword to search for KL trip interested (or type 'quit' to exit): ").lower().strip()

        if search_term == "quit":
            print("Exiting search.")
            break

        if not search_term:
            print("Please enter a keyword.")
            continue

        matched_services = {
            service_id: info
            for service_id, info in services.items()
            if search_term in info['name'].lower() or search_term in info['description'].lower()
        }

        if matched_services:
            print("\nMatching services:\n")
            display_services(matched_services)
            break
        else:
            print("No matching services found. Please try a different keyword.")

# for traveller to login
def mainmenu():
    print("Welcome to the Trip Planner Application\n"
          "1. Login\n"
          "2. Exit\n")

# main loop for traveller to choose
def main():
    logged_in_user = None
    users, bookings, services, promotions = load_data()

    while True:
        if not logged_in_user:
            mainmenu()
            choice1 = input("\nYour choice: ")
            if choice1 == "1":
                logged_in_user = login(users)
            elif choice1 == "2":
                print("Exiting application.")
                break
            else:
                print("Invalid option, please try again")
        else:
            print(f"\nWelcome, {logged_in_user}\n"
                  "1. View Profile\n"
                  "2. Update Profile\n"
                  "3. Plan Trip\n"
                  "4. View Bookings\n"
                  "5. Logout\n"
                  "6. Exit\n")

            choice2 = input("Your choice: ")
            if choice2 == "1":
                print(users[logged_in_user])
            elif choice2 == "2":
                logged_in_user = update_profile(logged_in_user, users, bookings, services,promotions)
            elif choice2 == "3":
                plan_trip(logged_in_user, users, bookings, services, promotions)
            elif choice2 == "4":
                view_bookings_info(logged_in_user, bookings, services)
            elif choice2 == "5":
                break
            elif choice2 == "6":
                print("Exiting application.")
                break
            else:
                print("Invalid option, please try again")
            save_data(users, bookings, services,promotions)

# run main loop
def travellerloop():
    main()

if __name__ == "__main__":
    main()