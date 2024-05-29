Banking Application


This Banking Application is a Python-based application that allows users to perform various banking operations such as logging in, viewing account details, card details, beneficiary details, adding beneficiaries, and transferring funds. 
It uses a MySQL database to store and retrieve user information and other banking details.

Features

1. User Authentication: Login with username and password.
2. View User Details: Retrieve and display user information.
3. View Account Details: Retrieve and display account information.
4. View Card Details: Retrieve and display card details.
5. View Beneficiary Details: Retrieve and display beneficiary information.
6. Add Beneficiary: Add a new beneficiary to the user's account.
7. Fund Transfer: Transfer funds between accounts.


Setup Instructions

Clone the Repository
bash
Copy code
git clone https://github.com/vish330/Banking-Application.git
cd banking-application

Create a Virtual Environment and Activate It
bash
Copy code
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`

Install Dependencies
bash
Copy code
pip install -r requirements.txt

Setup MySQL Database
Ensure you have a MySQL server running and create a database for the application. Update the mysql_connection.py file with your database credentials.

Run the Application
bash
Copy code
python -m code_files.main


Usage
1.Login
Enter the username and password to login.
2.View User Details
Option 1: Display user information such as username, full name, address, aadhar, mobile number, and email.
3.View Account Details
Option 2: Display account information such as account type, balance, and creation date.
4.View Card Details
Option 3: Display card details such as card number, card type, CVV, expiry date, and MPIN.
5.View Beneficiary Details
Option 4: Display beneficiary information such as beneficiary name, account number, bank, and IFSC.
6.Add Beneficiary
Option 5: Add a new beneficiary to the user's account.
Transfer Funds
Option 6: Transfer funds from one account to another.




