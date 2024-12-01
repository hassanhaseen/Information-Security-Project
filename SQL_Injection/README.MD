# SQL Injection Demo Project

## Overview

This project demonstrates a web-based login system vulnerable to SQL injection and then shows how to secure it. Built using Python's Flask framework and SQLite, this project aims to educate developers on the dangers of SQL injection and best practices for securing web applications.

![Login Page Screenshot](https://i.imgur.com/ZEfFay2.png)

## Features

- Web-based login page.
- Demonstrates the risks of SQL injection and how to mitigate them.
- Provides both insecure and secure implementations for educational purposes.

## Tech Stack

- **Frontend**: HTML, CSS (with dark mode styling)
- **Backend**: Flask (Python)
- **Database**: SQLite

## Getting Started

### Prerequisites

- Python 3.x
- Flask

### Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/hassanhaseen/Information-Security-Project/tree/main/SQL_Injection
    ```
2. **Navigate to the Project Directory**:
    ```sh
    cd SQL_Injection
    ```
3. **Install Flask**:
    ```sh
    pip install flask
    ```

### Running the Application

1. **Initialize the Database and Start the Server**:
    ```sh
    python app.py
    ```
2. **Access the Application**:
   - Open your browser and navigate to: `http://127.0.0.1:5000/`

## Usage

- **Login with Default Credentials**:
  - Username: `admin`
  - Password: `password123`

- **Testing SQL Injection (Insecure Version) [Use app\.py]**:
  - In the vulnerable version, you could try SQL injection strings like:
    ```
    ' OR 1=1--
    ```
  - The above should bypass login if the application is vulnerable.

- **Testing Security (Secure Version) [Use app1.py]**:
  - In the secure version, SQL injection attempts will fail.
  - User input is sanitized.

## Security Features

- **Parameterized Queries**: SQL queries are parameterized to prevent SQL injection attacks.


## Learnings and Key Takeaways

This project serves as an educational tool for understanding both vulnerabilities in web applications and how to secure them. Here are some key takeaways:

1. **SQL Injection Vulnerabilities**: It's crucial to avoid directly inserting user input into SQL queries without proper sanitization.
2. **Parameterized Queries**: Always use parameterized queries to mitigate SQL injection risks.

## Contributing

Feel free to submit issues or pull requests if you'd like to contribute to this project. Contributions are always welcome!

## License

- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
- Intentionally made for Educational Purposes Only.


