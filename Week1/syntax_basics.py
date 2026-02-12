# Function example

def greet_user():
    name = input("Enter your name: ")
    print("Hello", name)

def add_numbers():
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    print("Total:", num1 + num2)

# Program menu
while True:
    print("\nChoose an option:")
    print("1 - Greet user")
    print("2 - Add numbers")
    print("3 - Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        greet_user()

    elif choice == "2":
        add_numbers()

    elif choice == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid option")
