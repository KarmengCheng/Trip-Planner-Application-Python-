import json


# Function to load the admin database from a JSON file
def load_admin_database():
    try:
        with open('admin_database.json') as f:
            print("Admin database found and run successfully!")
            return json.load(f)
    except FileNotFoundError:
        print("Admin database file not found.")
    except json.JSONDecodeError:
        print("Encounter Error when decoding admin database JSON file")
    return None


# Function to handle the admin login process
def login(admin_database):
    if not admin_database:
        print("Failed to load admin database.")
        return False

    # Implement a loop to ensure valid input for login choice
    while True:
        perform_login = input("Do you want to login (Y/N)?: ").upper()
        if perform_login in ["Y", "N"]:
            break
        print("Invalid input. Please enter only Y or N.")

    if perform_login == "N":
        print("Exiting...")
        return False

    # Loop to ensure valid username input
    login_name = input("Enter your Username: ")
    while login_name not in admin_database:
        print("Username is not found!")
        login_name = input("Please re-enter your Username: ")

    # Loop to ensure valid password input
    while True:
        login_password = input("Enter your Password: ")
        if login_password == admin_database[login_name]["password"]:
            print("You have successfully logged in!\n")
            return True
        print("Password is incorrect!")


# This is the main menu
def system_interface(logged_in):
    if not logged_in:
        print("You are not logged in. Please attempt to login to access the panel.")
        return

    print("Welcome to the system administrator interface!\n")
    print("Please select an option by typing the corresponding number\n")
    print("1. Traveller Management")
    print("2. Merchant Management")
    print("3. Trip Recommendation Management")
    print("4. Promotion Management")
    print("5. Log out\n")

    # Loop to ensure valid menu option input
    while True:
        try:
            option = int(input("Enter the number of your option: "))
            if 1 <= option <= 5:
                break
            print("Invalid option. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    # Call the corresponding management function based on user input
    if option == 1:
        traveller_management()
    elif option == 2:
        merchant_management()
    elif option == 3:
        trip_recommendation_management()
    elif option == 4:
        promotion_management()
    elif option == 5:
        print("Logging out...")
        return False
    return True


# Function to load the main database from a JSON file
def load_database():
    try:
        with open('database.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Database file not found.")
    except json.JSONDecodeError:
        print("Encounter Error when decoding database JSON file")
    return None


# Function to save the main database to a JSON file
def save_database(data):
    try:
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Encounter Error saving database JSON file: {e}")


# Function to manage travellers
def traveller_management():
    data = load_database()
    if not data:
        return

    while True:
        print("You are in traveller management. Please choose your option\n")
        print("1. View traveller's information\n2. View currently blocked travellers\n3. Block traveller\n4. Unblock traveller\n5. Exit\n")

        # Loop to ensure valid menu option input
        try:
            sub_option = int(input("Enter the number of your option: "))
            if 1 <= sub_option <= 5:
                if sub_option == 1:
                    display_travellers(data['users'])
                elif sub_option == 2:
                    view_blocked_travellers(data['users'])
                elif sub_option == 3:
                    traveller_username = input("Enter the traveller username to block: ")
                    block_traveller(data['users'], traveller_username)
                    save_database(data)
                elif sub_option == 4:
                    traveller_username = input("Enter the traveller username to unblock: ")
                    unblock_traveller(data['users'], traveller_username)
                    save_database(data)
                elif sub_option == 5:
                    print("Exiting traveller management...")
                    break
            else:
                print("Invalid option. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")


# Function to display travelers
def display_travellers(users):
    for username, user_info in users.items():
        if user_info['role'] == 'traveller':
            print(f"Name: {username}, Status: {user_info['status']}, Password: {user_info['password']}")


def block_traveller(users, username):
    if username in users and users[username]['role'] == 'traveller':
        users[username]['status'] = 'Blocked'
        save_database({'users': users})  # Save changes to the database
        print(f"Traveller {username} has been blocked.")
    else:
        print(f"Traveller {username} not found or not a traveller.")


def unblock_traveller(users, username):
    if username in users and users[username]['role'] == 'traveller':
        users[username]['status'] = 'Active'
        save_database({'users': users})  # Save changes to the database
        print(f"Traveller {username} has been unblocked.")
    else:
        print(f"Traveller {username} not found or not a traveller.")


# Function to view blocked travellers
def view_blocked_travellers(users):
    blocked_users = [user for user, info in users.items() if info['role'] == 'traveller' and info['status'] == 'Blocked']
    if blocked_users:
        print("Blocked Travellers:")
        for user in blocked_users:
            print(f"{user}\n")
    else:
        print("No travellers are currently blocked.\n")


# Function to manage merchants
def merchant_management():
    data = load_database()
    if not data:
        return

    while True:
        print("You are in merchant management. Please choose your option\n")
        print("1. View merchant's information\n2. View currently blocked merchants\n3. Add a new merchant\n4. Block merchant\n5. Unblock merchant\n6. Exit\n")

        # Loop to ensure valid menu option input
        try:
            sub_option = int(input("Enter the number of your option: "))
            if 1 <= sub_option <= 6:
                if sub_option == 1:
                    display_merchants(data['users'])
                elif sub_option == 2:
                    view_blocked_merchants(data['users'])
                elif sub_option == 3:
                    add_merchant()
                    data = load_database()  # Reload the data to ensure it's updated
                elif sub_option == 4:
                    merchant_username = input("Enter the merchant username to block: ")
                    block_merchant(data['users'], merchant_username)
                    save_database(data)
                elif sub_option == 5:
                    merchant_username = input("Enter the merchant username to unblock: ")
                    unblock_merchant(data['users'], merchant_username)
                    save_database(data)
                elif sub_option == 6:
                    print("Exiting merchant management...")
                    break
            else:
                print("Invalid option. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")


# Function to display merchants
def display_merchants(users):
    for username, user_info in users.items():
        if user_info['role'] == 'merchant':
            print(f"Name: {username}, Status: {user_info['status']}, Password: {user_info['password']}, Merchant ID: {user_info['id']}")


# Function to find the next available merchant ID
def find_next_merchant_id(users):
    next_merchant_id = 0
    for user in users.values():
        if user['role'] == 'merchant' and user.get('id', 0) > next_merchant_id:
            next_merchant_id = user['id']
    return next_merchant_id + 1


def add_merchant():
    data = load_database()
    if data:
        username = input("Enter merchant username: ")
        password = input("Enter merchant password: ")

        # Check if the username already exists
        if username in data['users']:
            print("Merchant username already exists.")
            return

        # Find the next available merchant ID
        merchant_id = find_next_merchant_id(data['users'])

        # Add the new merchant to the users section
        data['users'][username] = {
            'password': password,
            'role': 'merchant',
            'id': merchant_id,
            'status': 'Active'
        }

        save_database(data)
        print(f"Merchant with username {username} and ID {merchant_id} has been added.")
        display_merchants(data['users'])  # Display the updated list of merchants



# Function to block merchant
def block_merchant(users, username):
    if username in users and users[username]['role'] == 'merchant':
        users[username]['status'] = 'Blocked'
        save_database({'users': users})  # Save changes to the database
        print(f"Merchant {username} has been blocked.")
    else:
        print(f"Merchant {username} not found or not a merchant.")


# Function to  unblock merchant
def unblock_merchant(users, username):
    if username in users and users[username]['role'] == 'merchant':
        users[username]['status'] = 'Active'
        save_database({'users': users})  # Save changes to the database
        print(f"Merchant {username} has been unblocked.")
    else:
        print(f"Merchant {username} not found or not a merchant.")


# Function to view blocked merchants
def view_blocked_merchants(users):
    blocked_users = [user for user, info in users.items() if info['role'] == 'merchant' and info['status'] == 'Blocked']
    if blocked_users:
        print("Blocked Merchants:")
        for user in blocked_users:
            print(f"{user}\n")
    else:
        print("No merchants are currently blocked.\n")


# Function to manage trip recommendations
def trip_recommendation_management():
    while True:
        print("You are in trip recommendation management. Please choose your option\n")
        print("1. View trip recommendations\n2. Provide trip recommendation\n3. Delete trip recommendation\n4. Update trip recommendation\n5. Exit\n")

        # Loop to ensure valid menu option input
        try:
            sub_option = int(input("Enter the number of your option: "))
            if 1 <= sub_option <= 5:
                if sub_option == 1:
                    view_trip_recommendations()
                elif sub_option == 2:
                    provide_trip_recommendation()
                elif sub_option == 3:
                    delete_trip_recommendation()
                elif sub_option == 4:
                    update_trip_recommendation()
                elif sub_option == 5:
                    print("Exiting trip recommendation management...")
                    break
            else:
                print("Invalid option. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")


# Function to load trip recommendations from a JSON file
def load_trip_recommendations():
    try:
        with open('database.json') as f:
            data = json.load(f)
            return data.get('triprecommendations', {}).get('destinations', [])
    except FileNotFoundError:
        print("Trip recommendations file not found.")
    except json.JSONDecodeError:
        print("Error decoding trip recommendations JSON file.")
    return []


# Function to save trip recommendations to a JSON file
def save_trip_recommendations(trip_recommendations):
    try:
        with open('database.json') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'triprecommendations': {'destinations': [], 'promotions': []}}

    data['triprecommendations']['destinations'] = trip_recommendations

    try:
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving trip recommendations: {e}")


# Function to view trip recommendations
def view_trip_recommendations():
    trip_recommendations = load_trip_recommendations()
    if trip_recommendations:
        print("Trip Recommendations:")
        for trip in trip_recommendations:
            print(
                f"Destination: {trip['name']}\n"
                f"Description: {trip['description']}\n"
                f"Attractions: {', '.join(trip['attractions'])}\n"
            )
    else:
        print("No trip recommendations available.")


# Function to provide a new trip recommendation
def provide_trip_recommendation():
    trip_recommendations = load_trip_recommendations()
    new_trip = {
        "name": input("Enter destination: ").capitalize(),
        "description": input("Enter trip description: "),
        "attractions": [attraction.strip() for attraction in input("Enter attractions (comma separated): ").split(',')]
    }
    trip_recommendations.append(new_trip)
    save_trip_recommendations(trip_recommendations)
    print("Trip recommendation provided successfully.")


# Function to delete a trip recommendation
def delete_trip_recommendation():
    trip_recommendations = load_trip_recommendations()
    destination = input("Enter destination to delete: ").capitalize()
    if any(trip['name'] == destination for trip in trip_recommendations):
        trip_recommendations = [trip for trip in trip_recommendations if trip['name'] != destination]
        save_trip_recommendations(trip_recommendations)
        print("Trip recommendation deleted successfully.")
    else:
        print("Destination not found.")


def update_trip_recommendation():
    trip_recommendations = load_trip_recommendations()
    destination = input("Enter destination to update: ").lower()
    for trip in trip_recommendations:
        if trip['name'].lower() == destination:
            trip['description'] = input("Enter new trip description: ")
            trip['attractions'] = [attraction.strip() for attraction in input("Enter new attractions (comma separated): ").split(',')]
            save_trip_recommendations(trip_recommendations)
            print("Trip recommendation updated successfully.\n")
            return
    print("Trip recommendation not found.\n")


# Function to manage promotions
def promotion_management():
    while True:
        print("You are in promotion management. Please choose your option\n")
        print("1. View promotions\n2. Add promotion\n3. Delete promotion\n4. Update promotion\n5. Exit\n")

        # Loop to ensure valid menu option input
        try:
            sub_option = int(input("Enter the number of your option: "))
            if 1 <= sub_option <= 5:
                if sub_option == 1:
                    view_promotions()
                elif sub_option == 2:
                    add_promotion()
                elif sub_option == 3:
                    delete_promotion()
                elif sub_option == 4:
                    update_promotion()
                elif sub_option == 5:
                    print("Exiting promotion management...")
                    break
            else:
                print("Invalid option. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")


# Function to load promotions from a JSON file
def load_promotions():
    try:
        with open('database.json') as f:
            data = json.load(f)
            return data.get('triprecommendations', {}).get('promotions', [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading promotions.")
    return []


# Function to save promotions to a JSON file
def save_promotions(promotions):
    try:
        with open('database.json') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {'triprecommendations': {'destinations': [], 'promotions': []}}

    data['triprecommendations']['promotions'] = promotions

    try:
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving promotions: {e}")


# Function to view promotions
def view_promotions():
    promotions = load_promotions()
    if promotions:
        print("Promotions:")
        for promo in promotions:
            print(
                f"Promo Code: {promo['promo_code']}\n"
                f"Title: {promo['title']}\n"
                f"Description: {promo['description']}\n"
                f"Discount: {promo['discount']}\n"
                f"Valid Month: {promo['valid_month']}\n"
            )
    else:
        print("No promotions available.")


# Function to add a new promotion
def add_promotion():
    promotions = load_promotions()
    new_promo = {
        "promo_code": input("Enter promo code: ").upper(),
        "title": input("Enter promotion title: "),
        "description": input("Enter promotion description: "),
        "discount": input("Enter discount: "),
        "valid_month": input("Enter valid month: ")
    }
    promotions.append(new_promo)
    save_promotions(promotions)
    print("Promotion added successfully.")


# Function to delete a promotion
def delete_promotion():
    promotions = load_promotions()
    promo_code = input("Enter promo code to delete: ").upper()
    if any(promo['promo_code'] == promo_code for promo in promotions):
        promotions = [promo for promo in promotions if promo['promo_code'] != promo_code]
        save_promotions(promotions)
        print("Promotion deleted successfully.")
    else:
        print("Promo code not found.")


# Function to update an existing promotion
def update_promotion():
    promotions = load_promotions()
    promo_code = input("Enter promo code to update: ").upper()
    for promo in promotions:
        if promo['promo_code'] == promo_code:
            promo['title'] = input("Enter new promotion title: ")
            promo['description'] = input("Enter new promotion description: ")
            promo['discount'] = input("Enter new promotion discount: ")
            promo['valid_month'] = input("Enter new valid month: ")
            save_promotions(promotions)
            print("Promotion updated successfully.\n")
            return
    print("Promotion not found.\n")


# This is the main function to handle the flow of the program
def main():
    admin_database = load_admin_database()
    logged_in = login(admin_database)
    while logged_in:
        logged_in = system_interface(logged_in)


# This is the entry point of the program to call the main function
if __name__ == "__main__":
    main()
