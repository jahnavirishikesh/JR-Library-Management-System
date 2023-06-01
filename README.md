# JR Library Management System

## Description
The JR Library Management System is a Python-based application that allows users to manage books, customers, and transactions in a library. It utilizes MySQL for data storage and retrieval. The system provides various functionalities such as adding and removing books, issuing and returning books for customers, searching books by ISBN, author name, or title name, managing customers, and retrieving customer IDs.

The data related to books, customers, and transactions is stored in CSV files located in a directory.

## Features
1. Python and MySQL: The system is written in Python and uses MySQL for data management.
2. CSV Data Storage: The data regarding books, customers, and transactions is stored in CSV files within a specific directory.
3. Book Management: Users can add new books to the library, remove existing books, and search for books by ISBN, author name, or title name.
4. Customer Management: The system allows the addition and removal of customers. Users can also search for customers and retrieve their IDs.
5. Transaction Handling: Customers can issue books and return them as needed.
6. User-Friendly Interface: The system provides an easy-to-use interface with clear instructions for performing various functions.

## Requirements
- Python 3.x
- MySQL
- Required Python packages:
  - pandas (for CSV data management)
  - mysql-connector-python (for MySQL database connectivity)

## Usage
1. Install Python and MySQL if not already installed on your system.
2. Create a MySQL database and configure the necessary tables for book, customer, and transaction management.
3. Clone this repository to your local machine.
4. Install the required Python packages by running the following command:
   ```
   pip install pandas mysql-connector-python
   ```
5. Update the MySQL connection details in the application code to match your database configuration.
6. Launch the application by running the main Python file:
   ```
   python JRLibraryApp.py
   ```
7. Follow the instructions provided by the application's user interface to perform various functions such as adding/removing books, managing customers, and handling transactions.

Feel free to explore the code and modify it to suit your specific needs. Happy library management!

## License
This project is licensed under the [MIT License](LICENSE).
