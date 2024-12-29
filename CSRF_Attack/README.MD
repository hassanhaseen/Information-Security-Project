# CSRF Attack Demonstration Project

## What is CSRF Attack?
CSRF (Cross-Site Request Forgery) is an attack where a victim is tricked into performing unauthorized actions on a website they are logged into, using their own credentials. The attacker sends a malicious request that exploits the victim’s authenticated session. Protection methods include using anti-CSRF tokens, SameSite cookies, and referer validation.

## Overview

This project demonstrates the vulnerabilities of web applications to **Cross-Site Request Forgery (CSRF)** attacks. It showcases how a malicious actor can exploit CSRF to perform unauthorized actions and emphasizes the importance of securing web applications against such attacks.

The project simulates a simple banking system where users can transfer money. By crafting a malicious page, it demonstrates how an attacker can trick a logged-in user into performing unintended actions.

![Login Page Screenshot](https://i.imgur.com/gAGYCtJ.png)
![CSRF Attack Page Screenshot](https://i.imgur.com/4RNy2iL.png)
![Transfer Money Page Screenshot](https://i.imgur.com/Dhdac8A.png)
---

## Features

- **Login System**: A basic login page where users can enter their credentials.
- **Transfer Money**: A feature to send money to another user.
- **Transaction History**: Displays a list of all past transactions.
- **CSRF Attack Simulation**: Demonstrates how CSRF attacks can exploit unprotected endpoints.

---

## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Flask (Python)
- **Database**: SQLite

---

## How It Works

### 1. Vulnerable Application
- A user logs in and navigates to a page to transfer money.
- The `/transfer` endpoint accepts POST requests without verifying their source, making it vulnerable to CSRF attacks.

### 2. CSRF Attack Simulation
- A malicious HTML page (`csrf_attack.html`) is crafted to exploit the vulnerability.
- When the victim, already logged in, interacts with the malicious page, the money is transferred to the attacker's account without the victim's knowledge.

### 3. Transaction History
- All transfer details are saved in an SQLite database and can be viewed on the `/transactions` page.

---

## Installation and Setup

### Prerequisites
- Python 3.x
- Flask

### Steps to Run the Project
1. **Clone the Repository**
   ```bash
   git clone https://github.com/hassanhaseen/Information-Security-Project/tree/main/CSRF_Attack
   cd CSRF_Attack
   ```
2. **Install Dependencies**
   ```bash
   pip install flask
   ```
3. **Initialize the Database**
   The database (`database.db`) is automatically created and initialized when you run the app for the first time.
4. **Run the Application**
   ```bash
   python app.py
   ```
5. **Access the Application**
   - Open your browser and navigate to `http://127.0.0.1:5000/`.
6. **Perform CSRF Attack**
   - Open `csrf_attack.html` directly in your browser.
   - Click the malicious button to trigger the attack.

### Key Features and Learnings
1. **CSRF Attack Vulnerabilities**:
   - Demonstrates how unprotected POST endpoints are susceptible to CSRF attacks.
   - Shows the potential damage caused by maliciously crafted pages.

2. **Transaction History**:
   - Tracks all transactions in the SQLite database.
   - Provides a transparent view of actions performed in the application.

### Protection Against CSRF Attack:-
1. **Use Anti-CSRF Tokens**:
   - Anti-CSRF tokens are random values generated for every user session and included in forms or requests. The server verifies the token when the form is submitted to ensure the request is legitimate.

2. **Use SameSite Cookies**:
   - Modern browsers support a cookie attribute called SameSite. It prevents cookies from being sent along with cross-site requests. You can set the SameSite attribute to Strict or Lax to prevent cookies from being sent with cross-origin requests.

3. **Check the Referer Header**:
   - The Referer header identifies the origin of the request. You can check if the referer is from your own domain before allowing sensitive actions like money transfers or changing user details.

4. **Content Security Policy (CSP):**
   - A CSP is a security feature that helps to prevent attacks like CSRF and XSS by restricting where resources can be loaded from. It can be used to ensure that only trusted sources are allowed to submit requests to your application.

5. **Disable HTTP Methods Like DELETE and PUT in Forms:**
   - Ensure that sensitive HTTP methods like DELETE and PUT are only accessible through secure, authenticated requests. Avoid exposing such methods via forms directly, and if necessary, validate the method through the HTTP header.
 
6. **Implement Same-Origin Policy**
   - Ensure that your site only accepts requests originating from the same domain (origin). This is done by checking the Origin header and rejecting requests that come from outside your domain.

 - You can implement CSRF Protection using any combination of these techniques, but the Anti-CSRF Tokens and SameSite Cookies offer the most effective and widely supported defense against CSRF attacks. To implement a fully secure app, combine these methods with strong session management and HTTPS to protect data during transit.



### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to create a pull request or open an issue.

### License
- This project is licensed under the MIT License. Feel free to use it for educational purposes!
- Intentionally made for Educational Purposes Only.
