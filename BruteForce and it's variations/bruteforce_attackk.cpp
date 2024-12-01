#include <iostream>
#include <string>
#include <ctime>
#include <cstdlib>

using namespace std;

// Define the character set for the brute-force search
const string charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[{]}|;:'\",<.>/?";

// Function to simulate password check 
bool checkPassword(const string& username, const string& passwordAttempt) {
    string correctPassword = "aaaaabcc";  // Ideal 8-character password for username "anosh1121"
    return passwordAttempt == correctPassword;
}

// Function to generate the next password attempt in lexicographic order
bool nextPassword(string& passwordAttempt) {
    int n = passwordAttempt.length();
    int idx = n - 1;

    while (idx >= 0) {
        size_t pos = charset.find(passwordAttempt[idx]);
        if (pos == charset.length() - 1) {
            passwordAttempt[idx] = charset[0];  // Reset to first character
            idx--;
        }
        else {
            passwordAttempt[idx] = charset[pos + 1];  // Increment to next character
            return true;
        }
    }
    return false;  // All combinations have been tried
}

int main() {
    string username = "anosh1121"; // Username
    string passwordAttempt = "aaaaaaaa"; // Starting password attempt (all 'a's)
    int attemptCount = 0;           // Counter for number of attempts

    clock_t startTime = clock();    // Start timer to track brute-force duration

    // Brute-force loop for 8-character password cracking
    while (nextPassword(passwordAttempt)) {
        attemptCount++;

        // Print each password attempt
        cout << "Attempt #" << attemptCount << ": " << passwordAttempt << endl;

        // Check if this password is correct
        if (checkPassword(username, passwordAttempt)) {
            clock_t endTime = clock();  // End timer when password is found
            double timeSpent = double(endTime - startTime) / CLOCKS_PER_SEC;

            cout << "\nPassword found! The correct password for username '" << username << "' is: " << passwordAttempt << endl;
            cout << "Total attempts: " << attemptCount << endl;
            cout << "Time taken: " << timeSpent << " seconds." << endl;
            return 0;
        }
    }

    cout << "\nPassword not found after " << attemptCount << " attempts." << endl;
    return 0;
}

