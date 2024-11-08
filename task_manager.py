import hashlib

# File paths
USER_DATA_FILE = 'users.txt'
TASK_DATA_FILE = 'tasks.txt'

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    """Register a new user with a unique username and hashed password."""
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    hashed_password = hash_password(password)

    # Check if the username already exists
    user_exists = False
    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = file.readlines()
            for line in users:
                if line.strip().split(',')[0] == username:
                    user_exists = True
                    break
    except FileNotFoundError:
        pass  # If the file doesn't exist, we can create a new user

    if user_exists:
        print("Username already exists. Please choose a different username.")
        return

    # Store the new user
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{hashed_password}\n")
    print("Registration successful!")

def login_user():
    """Log in an existing user."""
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    try:
        with open(USER_DATA_FILE, 'r') as file:
            users = file.readlines()
            for line in users:
                user, pwd = line.strip().split(',')
                if user == username and pwd == hashed_password:
                    print("Login successful!")
                    return username
    except FileNotFoundError:
        print("No users found. Please register first.")
        return None

    print("Invalid username or password.")
    return None

def add_task(username):
    """Add a new task for the logged-in user."""
    task_description = input("Enter the task description: ")
    task_id = generate_task_id(username)
    task = f"{username},{task_id},{task_description},Pending\n"

    # Store the task in the tasks file
    with open(TASK_DATA_FILE, 'a') as file:
        file.write(task)
    print("Task added successfully!")

def generate_task_id(username):
    """Generate a unique task ID based on the current tasks."""
    try:
        with open(TASK_DATA_FILE, 'r') as file:
            tasks = file.readlines()
            user_tasks = [task for task in tasks if task.startswith(username)]
            return len(user_tasks) + 1
    except FileNotFoundError:
        return 1  # If no tasks exist, start with ID 1

def view_tasks(username):
    """View all tasks for the logged-in user."""
    try:
        with open(TASK_DATA_FILE, 'r') as file:
            tasks = file.readlines()
            user_tasks = [task for task in tasks if task.startswith(username)]
            if not user_tasks:
                print("No tasks found.")
                return
            for task in user_tasks:
                task_id, description, status = task.strip().split(',')[1:]
                print(f"ID: {task_id}, Description: {description}, Status: {status}")
    except FileNotFoundError:
        print("No tasks found.")

def mark_task_completed(username):
    """Mark a task as completed."""
    task_id = input("Enter the task ID to mark as completed: ")
    try:
        with open(TASK_DATA_FILE, 'r') as file:
            tasks = file.readlines()

        with open(TASK_DATA_FILE, 'w') as file:
            task_found = False
            for task in tasks:
                if task.startswith(username):
                    tid, description, status = task.strip().split(',')[1:]
                    if tid == task_id:
                        status = 'Completed'
                        task_found = True
                    file.write(f"{username},{tid},{description},{status}\n")
                else:
                    file.write(task)
            if task_found:
                print("Task marked as completed!")
            else:
                print("Task ID not found.")
    except FileNotFoundError:
        print("No tasks found.")

def delete_task(username):
    """Delete a task by its ID."""
    task_id = input("Enter the task ID to delete: ")
    try:
        with open(TASK_DATA_FILE, 'r') as file:
            tasks = file.readlines()

        with open(TASK_DATA_FILE, 'w') as file:
            task_found = False
            for task in tasks:
                if task.startswith(username):
                    tid, description, status = task.strip().split(',')[1:]
                    if tid == task_id:
                        task_found = True
                        continue  # Skip writing this task
                file.write(task)
            if task_found:
                print("Task deleted successfully!")
            else:
                print("Task ID not found.")
    except FileNotFoundError:
        print("No tasks found.")

def menu():
    """Main function to run the task manager."""
    while True:
        print("\nWelcome to the Task Manager!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                while True:
                    print("\nMenu:")
                    print("1. Add Task")
                    print("2. View Tasks")
                    print("3. Mark Task as Completed")
                    print("4. Delete Task")
                    print("5. Logout")
                    
                    menu_choice = input("Choose an option (1-5): ")
                    
                    if menu_choice == '1':
                        add_task(username)
                    elif menu_choice == '2':
                        view_tasks(username)
                    elif menu_choice == '3':
                        mark_task_completed(username)
                    elif menu_choice == '4':
                        delete_task(username)
                    elif menu_choice == '5':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice, please try again.")
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

menu()