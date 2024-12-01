#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <mutex>
#include <thread> // Include thread library

using namespace std;

// Character set for brute force
const string charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

// Password checker simulation
bool checkPassword(const string& username, const string& passwordAttempt) {
    string correctPassword = "aaaaabcc"; // Target password
    return passwordAttempt == correctPassword;
}

// Shared mutex to synchronize found password
mutex mtx;
bool found = false;
string foundPassword = "";

// Function to brute force within a given range
void bruteForceRange(size_t startIdx, size_t endIdx, int maxLength) {
    string password(maxLength, charset[0]);
    size_t charsetSize = charset.size();

    // Initialize to startIdx
    for (int i = 0; i < maxLength; ++i) {
        size_t idx = (startIdx / static_cast<size_t>(pow(charsetSize, i))) % charsetSize;
        password[i] = charset[idx];
    }

    while (!found && startIdx < endIdx) {
        // Check password
        if (checkPassword("anosh1121", password)) {
            lock_guard<mutex> lock(mtx);
            found = true;
            foundPassword = password;
            return;
        }

        // Increment to next password
        for (int i = maxLength - 1; i >= 0; --i) {
            size_t charIdx = charset.find(password[i]);
            if (charIdx < charsetSize - 1) {
                password[i] = charset[charIdx + 1];
                break;
            }
            else {
                password[i] = charset[0];
            }
        }
        ++startIdx;
    }
}

int main() {
    int maxLength = 8;
    size_t charsetSize = charset.size();
    size_t totalPasswords = static_cast<size_t>(pow(charsetSize, maxLength));
    int numThreads = 4;

    // Divide work among threads
    vector<thread> threads;
    size_t passwordsPerThread = totalPasswords / numThreads;

    for (int i = 0; i < numThreads; ++i) {
        size_t startIdx = i * passwordsPerThread;
        size_t endIdx = (i + 1) * passwordsPerThread;
        threads.emplace_back(bruteForceRange, startIdx, endIdx, maxLength);
    }

    // Join threads
    for (auto& t : threads) {
        t.join();
    }

    if (found) {
        cout << "Password found: " << foundPassword << endl;
    }
    else {
        cout << "Password not found." << endl;
    }

    return 0;
}
