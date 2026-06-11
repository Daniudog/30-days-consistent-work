new_pwd = input("Set the master password: ")
pwd = input("What is the master password?: ")
if new_pwd != pwd:
    print("Password is incorrect")

def view():
    print(f"The password is {new_pwd}")

def add():
    new = input("Enter a the master password to add anew password: ")
    if new == pwd:
        new_pwd = input("Enter a new password: ")
    else:
        print("Password is incorrect")


while True:
    mode = input("Would you like to add a new password or view existing ones? (view, Add. Enter q to quit): ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()

    elif mode == "add":
        add()

    else:
        print("Invalid mode.")
        continue