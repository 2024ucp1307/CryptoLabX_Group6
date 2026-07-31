from utils.file_analysis import analyze_file
from utils.logger import write_log

def menu():
    while True:
        print("\n==============================")
        print("     CryptoLabX Toolkit")
        print("==============================")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze Dataset")
        print("5. Exit")

        choice = input("Enter your choice: ")

        write_log(choice)

        if choice == "1":
            print("\nEncrypt Module")
            print("Coming Soon...")

        elif choice == "2":
            print("\nDecrypt Module")
            print("Coming Soon...")

        elif choice == "3":
            print("\nAttack Module")
            print("Coming Soon...")

        elif choice == "4":
            filename = input("Enter dataset filename: ")
            analyze_file(filename)

        elif choice == "5":
            print("\nThank you for using CryptoLabX.")
            break

        else:
            print("\nInvalid Choice!")

if __name__ == "__main__":
    menu()
