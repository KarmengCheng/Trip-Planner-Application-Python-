import guest
import traveller
import merchant
import systemadministrator
def combinemenu():
    print(
        "Welcome to the Trip Planner Application, you want to\n"
        "1. Browse as guest\n"
        "2. Login as traveller\n"
        "3. Login as merchant\n"
        "4. Login as system administrator\n"
        "5. Exit")

def main():
    while True:
        combinemenu()
        choice1 = input("\nYour choice: ")
        if choice1 == "1":
            guest.guestloop()
        elif choice1 == "2":
            traveller.travellerloop()
        elif choice1 == "3":
            merchant.merchantloop()
        elif choice1 == "4":
            systemadministrator.main()
        elif choice1 == "5":
            exit_choice = input("Are you sure you want to exit? (yes/no): ").lower()
            if exit_choice == "yes":
                print("Thanks for using Trip Planner Application")
                break  # Exit the application
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()