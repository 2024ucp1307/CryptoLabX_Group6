# main.py

def show_menu():
    print("\n" + "=" * 40)
    print("       CryptoLabX Toolkit")
    print("=" * 40)
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")
    print("=" * 40)


def encrypt():
    print("\n[Encrypt]")
    print("Coming Soon...")


def decrypt():
    print("\n[Decrypt]")
    print("Coming Soon...")


def attack():
    print("\n[Attack]")
    print("Coming Soon...")


def analyze():
    print("\n[Analyze]")
    print("Coming Soon...")


def main():
    while True:
        show_menu()

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            encrypt()

        elif choice == "2":
            decrypt()

        elif choice == "3":
            attack()

        elif choice == "4":
            analyze()

        elif choice == "5":
            print("\nThank you for using CryptoLabX.")
            print("Exiting...")
            break

        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
