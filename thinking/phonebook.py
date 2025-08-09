#  Phone Book
def phone_book():
    contacts = {}
    while True:
        print("\n=== Phone Book ===")
        print("1. Add Contact\n2. Search Contact\n3. Delete Contact\n4. View All\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            number = input("Number: ")
            contacts[name] = number
            print("Contact added!")
        elif choice == "2":
            name = input("Name to search: ")
            print(f"{name}: {contacts.get(name, 'Not found')}")
        elif choice == "3":
            name = input("Name to delete: ")
            if name in contacts:
                del contacts[name]
                print("Deleted!")
            else:
                print("Contact not found.")
        elif choice == "4":
            if contacts:
                for name, number in contacts.items():
                    print(f"{name}: {number}")
            else:
                print("No contacts yet.")
        elif choice == "5":
            break
        else:
            print("Invalid choice.")