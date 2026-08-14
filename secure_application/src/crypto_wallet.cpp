#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Transaction {
    string type;
    string user;
    double amount;
};

struct Wallet {
    string username;
    string password;
    double balance;
    vector<Transaction> history;
};

vector<Wallet> wallets;

void createWallet() {
    string username, password;

    cout << "\n--- Create Wallet ---\n";
    cout << "Enter username: ";
    cin >> username;

    cout << "Enter password: ";
    cin >> password;

    Wallet newWallet;
    newWallet.username = username;
    newWallet.password = password;
    newWallet.balance = 10000;

    wallets.push_back(newWallet);

    cout << "Wallet created successfully!\n";
    cout << "Initial balance: " << newWallet.balance << "\n";
}

int login() {
    string username, password;

    cout << "\n--- Login ---\n";
    cout << "Username: ";
    cin >> username;

    cout << "Password: ";
    cin >> password;

    // Vulnerability 1: Hardcoded Secret
    string adminSecret = "CryptoAdmin@123";

    if (password == adminSecret) {
        cout << "Admin login successful!\n";

        for (int i = 0; i < wallets.size(); i++) {
            if (wallets[i].username == username) {
                return i;
            }
        }
    }

    for (int i = 0; i < wallets.size(); i++) {
        if (wallets[i].username == username &&
            wallets[i].password == password) {
            cout << "Login successful!\n";
            return i;
        }
    }

    // Vulnerability 2: Information Leakage
    cout << "Login failed!\n";
    cout << "DEBUG: Username entered = " << username << "\n";
    cout << "DEBUG: Password entered = " << password << "\n";

    return -1;
}

void checkBalance(int userIndex) {
    cout << "\n--- Balance ---\n";
    cout << "Wallet Owner: " << wallets[userIndex].username << "\n";
    cout << "Current Balance: " << wallets[userIndex].balance << "\n";
}

void sendTransaction(int userIndex) {
    string receiver;
    double amount;

    cout << "\n--- Send Transaction ---\n";
    cout << "Enter receiver username: ";
    cin >> receiver;

    cout << "Enter amount: ";
    cin >> amount;

    // Vulnerability 3: Improper Input Validation
    // No check for negative or zero amount

    if (amount <= wallets[userIndex].balance) {
        wallets[userIndex].balance -= amount;

        Transaction t;
        t.type = "Sent";
        t.user = receiver;
        t.amount = amount;

        wallets[userIndex].history.push_back(t);

        cout << "Transaction successful!\n";
        cout << "Sent " << amount << " to " << receiver << "\n";
        cout << "Remaining balance: "
             << wallets[userIndex].balance << "\n";
    } else {
        cout << "Insufficient balance!\n";
    }
}

void viewHistory(int userIndex) {
    cout << "\n--- Transaction History ---\n";

    if (wallets[userIndex].history.empty()) {
        cout << "No transactions found.\n";
        return;
    }

    for (int i = 0; i < wallets[userIndex].history.size(); i++) {
        cout << i + 1 << ". "
             << wallets[userIndex].history[i].type
             << " "
             << wallets[userIndex].history[i].amount
             << " to/from "
             << wallets[userIndex].history[i].user
             << "\n";
    }
}

void walletMenu(int userIndex) {
    int choice;

    while (true) {
        cout << "\n================================\n";
        cout << "       CRYPTO WALLET\n";
        cout << "================================\n";
        cout << "Logged in as: "
             << wallets[userIndex].username << "\n\n";

        cout << "1. Check Balance\n";
        cout << "2. Send Transaction\n";
        cout << "3. View Transaction History\n";
        cout << "4. Logout\n";
        cout << "Enter choice: ";

        cin >> choice;

        switch (choice) {
            case 1:
                checkBalance(userIndex);
                break;

            case 2:
                sendTransaction(userIndex);
                break;

            case 3:
                viewHistory(userIndex);
                break;

            case 4:
                cout << "Logged out successfully.\n";
                return;

            default:
                cout << "Invalid choice!\n";
        }
    }
}

int main() {
    // Sample wallets
    Wallet alice;
    alice.username = "alice";
    alice.password = "alice123";
    alice.balance = 10000;
    wallets.push_back(alice);

    Wallet bob;
    bob.username = "bob";
    bob.password = "bob123";
    bob.balance = 5000;
    wallets.push_back(bob);

    int choice;

    while (true) {
        cout << "\n================================\n";
        cout << "     CRYPTOCURRENCY WALLET\n";
        cout << "================================\n";
        cout << "1. Create Wallet\n";
        cout << "2. Login\n";
        cout << "3. Exit\n";
        cout << "Enter choice: ";

        cin >> choice;

        switch (choice) {
            case 1:
                createWallet();
                break;

            case 2: {
                int userIndex = login();

                if (userIndex != -1) {
                    walletMenu(userIndex);
                }

                break;
            }

            case 3:
                cout << "Thank you for using Crypto Wallet!\n";
                return 0;

            default:
                cout << "Invalid choice!\n";
        }
    }

    return 0;
}
