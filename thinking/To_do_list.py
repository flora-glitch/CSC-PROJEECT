# To-Do List
def todo_list():
    tasks = []
    while True:
        print("\n=== To-Do List ===")
        print("1. Add Task\n2. View Tasks\n3. Delete Task\n4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            print("Task added!")
        elif choice == "2":
            if tasks:
                for i, t in enumerate(tasks, 1):
                    print(f"{i}. {t}")
            else:
                print("No tasks yet.")
        elif choice == "3":
            try:
                num = int(input("Enter task number to delete: "))
                if 0 < num <= len(tasks):
                    tasks.pop(num-1)
                    print("Deleted!")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Enter a valid number.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
