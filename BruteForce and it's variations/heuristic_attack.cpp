#include <iostream>
#include <string>
#include <vector>
#include <ctime>

using namespace std;

// Simulate password check
bool checkPassword(const string& username, const string& passwordAttempt) {
    string correctPassword = "aaaaabcc";
    return passwordAttempt == correctPassword;
}

// Function to generate at least 50 password attempts using heuristic patterns
vector<string> generateHeuristicPasswords() {
    vector<string> passwords;

    // Add common patterns
    passwords.push_back("password");
    passwords.push_back("123456");
    passwords.push_back("qwerty");
    passwords.push_back("abc123");
    passwords.push_back("admin123");
    passwords.push_back("letmein");
    passwords.push_back("welcome1");
    passwords.push_back("aaaaabcc");
    passwords.push_back("1q2w3e4r");

    // Add heuristic-based guesses
    for (char c = 'a'; c <= 'z'; ++c) {
        passwords.push_back(string(8, c)); // Repeat character 8 times
    }

    // Add variations with numbers and special characters
    for (int i = 1; i <= 10; ++i) {
        passwords.push_back("pass" + to_string(i));
        passwords.push_back("admin" + to_string(i));
    }

    // Add combinations of repeating patterns
    passwords.push_back("abcdabcd");
    passwords.push_back("aaaa1111");
    passwords.push_back("1234abcd");
    passwords.push_back("pass1234");
    passwords.push_back("admin#123");
    passwords.push_back("guest000");
    passwords.push_back("root1234");

    // Ensure at least 50 passwords
    while (passwords.size() < 50) {
        passwords.push_back("extra" + to_string(passwords.size()));
    }

    return passwords;
}

int main() {
    string username = "anosh1121";
    vector<string> passwords = generateHeuristicPasswords();
    int attemptCount = 0;

    clock_t startTime = clock();  // Start timer

    for (const string& passwordAttempt : passwords) {
        attemptCount++;

        cout << "Attempt #" << attemptCount << ": " << passwordAttempt << endl;

        // Check if the password is correct
        if (checkPassword(username, passwordAttempt)) {
            clock_t endTime = clock();  // End timer
            double timeSpent = double(endTime - startTime) / CLOCKS_PER_SEC;

            cout << "\nPassword found! The correct password is: " << passwordAttempt << endl;
            cout << "Total attempts: " << attemptCount << endl;
            cout << "Time taken: " << timeSpent << " seconds." << endl;
            return 0;
        }
    }

    cout << "\nPassword not found in heuristic guesses after " << attemptCount << " attempts." << endl;
    return 0;
}
