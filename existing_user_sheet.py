
import hashlib
from mysql_connection import get_connection, close_connection
import pymysql
from additional_function import update_cells_empty


# Function to prompt for existing user details
def prompt_existing_user_details(registration):
    print("inside prompt_existing_user_details")
    registration.update_cell(5, 1, "Enter Username: ")
    registration.update_cell(6, 1, "Enter Your Password: ")
    registration.update_cell(7, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")
    print("outside prompt_existing_user_details")
    return

# Function to log in a customer and retrieve account information
def customer_login(username, password):
    print("inside customer_login")
    connection = get_connection()

    if connection is None:
        return {"status": "error", "message": "Unable to connect to the database"}

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            sql = """
            SELECT user_id, username, full_name, address, aadhar, mobile_no, email
            FROM Users
            WHERE username = %s AND password = %s
            """
            cursor.execute(sql, (username, hashed_password))
            user = cursor.fetchone()
            if user is None:
                return {"status": "error", "message": "Invalid username or password"}

            sql = """
            SELECT account_id, account_type, balance, created_at
            FROM Accounts
            WHERE user_id = %s
            """
            cursor.execute(sql, (user["user_id"],))
            accounts = cursor.fetchall()
            if not accounts:
                accounts = 'N/A'
            else:
                accounts = accounts[0]

            sql = """
            SELECT card_number, card_type, cvv, expiry_date, mpin
            FROM Cards
            WHERE account_id = %s
            """
            cursor.execute(sql, (accounts["account_id"],))
            cards = cursor.fetchall()
            if not cards:
                cards = 'N/A'
            else:
                cards = cards[0]

            sql = """
            SELECT beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc
            FROM Beneficiaries
            WHERE account_id = %s
            """
            cursor.execute(sql, (accounts["account_id"],))
            beneficiaries = cursor.fetchall()
            if not beneficiaries:
                beneficiaries = 'N/A'
            else:
                beneficiaries = beneficiaries[0]

            print("outside customer_login")
            return {
                "status": "success",
                "user": user,
                "accounts": accounts,
                "cards": cards,
                "beneficiaries": beneficiaries
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        close_connection(connection)

def after_login_option(registration):
    print("inside after_login_options")
    registration.update_cell(5, 1, "Choose from the below banking options")
    registration.update_cell(6, 1, "Type 1 in B5 cell to get user details")
    registration.update_cell(7, 1, "Type 2 in B5 cell to get account information")
    registration.update_cell(8, 1, "Type 3 in B5 cell to get card details")
    registration.update_cell(9, 1, "Type 4 in B5 cell to get beneficiary details")
    registration.update_cell(10, 1, "Type 5 in B5 cell to add new beneficiary details")
    registration.update_cell(11, 1, "Type 6 in B5 cell to transfer funds")
    registration.update_cell(12, 1, "Type anything in B5 cell to exit")
    registration.update_cell(5, 2, "____________________________")
    registration.update_cell(13, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")
    print("outside after_login_options")
    return

def transfer_funds(from_account_number, to_account_number, amount):
    connection = get_connection()
    print(from_account_number)
    print("*****")
    print(to_account_number) 
    if connection is None:
        return {"status": "error", "message": "Unable to connect to the database"}

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            connection.begin()
            
            # Fetch balance from source account
            cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE", (from_account_number,))
            from_account = cursor.fetchone()
            if from_account is None:
                return {"status": "error", "message": "Source account does not exist"}

            if from_account['balance'] < amount:
                return {"status": "error", "message": "Insufficient funds in the source account"}

            # Fetch balance from destination account
            cursor.execute("SELECT balance FROM Accounts WHERE account_id = %s FOR UPDATE", (to_account_number,))
            to_account = cursor.fetchone()
            if to_account is None:
                return {"status": "error", "message": "Destination account does not exist"}

            # Calculate new balances
            new_from_balance = from_account['balance'] - amount
            new_to_balance = to_account['balance'] + amount

            # Update source account balance
            cursor.execute("UPDATE Accounts SET balance = %s WHERE account_id = %s", (new_from_balance, from_account_number))

            # Update destination account balance
            cursor.execute("UPDATE Accounts SET balance = %s WHERE account_id = %s", (new_to_balance, to_account_number))

            # Insert the transaction record
            cursor.execute(
                "INSERT INTO transactions (from_acc, to_acc, amount, transaction_timestamp) VALUES (%s, %s, %s, NOW())",
                (from_account_number, to_account_number, amount)
            )

            # Commit the transaction
            connection.commit()
            return {"status": "success", "message": "Funds transferred successfully"}

    except Exception as e:
        connection.rollback()
        return {"status": "error", "message": str(e)}

    finally:
        close_connection(connection)

def handle_fund_transfer_prompt(registration):
    registration.update_cell(5, 1, "Enter from account number: ")
    registration.update_cell(6, 1, "Enter to account number: ")
    registration.update_cell(7, 1, "Enter amount to transfer: ")
    registration.update_cell(8, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")
    return

def process_fund_transfer(registration, from_account_number, to_account_number, amount):
    try:
        amount = float(amount)
    except ValueError:
        registration.update_cell(5, 1, "Invalid amount. Please enter a numeric value.")
        return

    result = transfer_funds(from_account_number, to_account_number, amount)
    if result["status"] == "success":
        registration.update_cell(5, 1, result["message"])
    else:
        registration.update_cell(5, 1, "Error: " + result["message"])

def user_datails(registration, option, result):
    print("inside user_datails")
    
    if option == '1':
        update_cells_empty(registration, 5, 11, 1, 2)
       
        data = result["user"]
        registration.update_cell(5, 1, "username")
        registration.update_cell(5, 2, data["username"])
        registration.update_cell(6, 1, "full_name")
        registration.update_cell(6, 2, data["full_name"])
        registration.update_cell(7, 1, "address")
        registration.update_cell(7, 2, data["address"])
        registration.update_cell(8, 1, "aadhar")
        registration.update_cell(8, 2, data["aadhar"])
        registration.update_cell(9, 1, "mobile_no")
        registration.update_cell(9, 2, data["mobile_no"])
        registration.update_cell(10, 1, "email")
        registration.update_cell(10, 2, data["email"])
        registration.update_cell(11, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
        
    elif option == '2':
        print("--------------------------------------------------------")
        data = result["accounts"]
        update_cells_empty(registration, 5, 11, 1, 2)
        if data == 'N/A':
            registration.update_cell(5, 1, "No details found")
            return
        
        registration.update_cell(5, 1, "account_type")
        registration.update_cell(5, 2, data["account_type"])
        registration.update_cell(6, 1, "balance")
        balance_as_float = float(data["balance"])
        registration.update_cell(6, 2, balance_as_float)
        registration.update_cell(7, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
        
    elif option == '3':
        data = result["cards"]
        update_cells_empty(registration, 5, 11, 1, 2)
        if data == 'N/A':
            registration.update_cell(5, 1, "No details found")
            return
        
        registration.update_cell(5, 1, "card_number")
        card_number = str(int(float(data["card_number"])))
        registration.update_cell(5, 2, card_number)
        registration.update_cell(6, 1, "card_type")
        registration.update_cell(6, 2, data["card_type"])
        registration.update_cell(7, 1, "cvv")
        registration.update_cell(7, 2, data["cvv"])
        registration.update_cell(8, 1, "expiry_date")
        expiry_date_str = data["expiry_date"].strftime("%Y-%m-%d")
        registration.update_cell(8, 2, expiry_date_str)
        registration.update_cell(9, 1, "mpin")
        registration.update_cell(9, 2, data["mpin"])
        registration.update_cell(10, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
        
    elif option == '4':
        data = result["beneficiaries"]
        update_cells_empty(registration, 5, 11, 1, 2)
        if data == 'N/A':
            registration.update_cell(5, 1, "No details found")
            return
        
        registration.update_cell(5, 1, "beneficiary_name")
        registration.update_cell(5, 2, data["beneficiary_name"])
        registration.update_cell(6, 1, "beneficiary_account_number")
        registration.update_cell(6, 2, data["beneficiary_account_number"])
        registration.update_cell(7, 1, "beneficiary_bank")
        registration.update_cell(7, 2, data["beneficiary_bank"])
        registration.update_cell(8, 1, "beneficiary_ifsc")
        registration.update_cell(8, 2, data["beneficiary_ifsc"])
        registration.update_cell(9, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
        
    elif option == '6':
        handle_fund_transfer_prompt(registration)
    else:
        update_cells_empty(registration, 5, 11, 1, 2)
        registration.update_cell(5, 3, "exit successfully")
        print('in else user_datails')
        return "Exit"
    
    print("outside user_datails")

def main_workflow(registration, option, result):
    if option == '6':
        from_account_number = registration.get_cell(5, 2).value
        to_account_number = registration.get_cell(6, 2).value
        amount = registration.get_cell(7, 2).value
        process_fund_transfer(registration, from_account_number, to_account_number, amount)
    else:
        user_datails(registration, option, result)



# import hashlib
# import pymysql
# from mysql_connection import get_connection, close_connection
# from additional_function import update_cells_empty
# # from user_details import get_user_details
# from account_info import get_account_info
# from card_details import get_card_details
# from beneficiary_details import get_beneficiary_details
# from add_beneficiary import add_new_beneficiary
# from transfer_funds import handle_fund_transfer_prompt, process_fund_transfer

# # Function to prompt for existing user details

# # Function to prompt for existing user details
# def prompt_existing_user_details(registration):
#     registration.update_cell(5, 1, "Enter Username: ")
#     registration.update_cell(6, 1, "Enter Your Password: ")
#     registration.update_cell(7, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")

# # Function to authenticate customer login and retrieve account information
# def customer_login(username, password):
#     connection = get_connection()
#     if connection is None:
#         return {"status": "error", "message": "Unable to connect to the database"}

#     try:
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             hashed_password = hashlib.sha256(password.encode()).hexdigest()
#             sql = """
#             SELECT user_id, username, full_name, address, aadhar, mobile_no, email
#             FROM Users
#             WHERE username = %s AND password = %s
#             """
#             cursor.execute(sql, (username, hashed_password))
#             user = cursor.fetchone()
#             if user is None:
#                 return {"status": "error", "message": "Invalid username or password"}

#             sql = """
#             SELECT account_id, account_type, balance, created_at
#             FROM Accounts
#             WHERE user_id = %s
#             """
#             cursor.execute(sql, (user["user_id"],))
#             accounts = cursor.fetchall()
#             accounts = accounts[0] if accounts else 'N/A'

#             sql = """
#             SELECT card_number, card_type, cvv, expiry_date, mpin
#             FROM Cards
#             WHERE account_id = %s
#             """
#             cursor.execute(sql, (accounts["account_id"],))
#             cards = cursor.fetchall()
#             cards = cards[0] if cards else 'N/A'

#             sql = """
#             SELECT beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc
#             FROM Beneficiaries
#             WHERE account_id = %s
#             """
#             cursor.execute(sql, (accounts["account_id"],))
#             beneficiaries = cursor.fetchall()
#             beneficiaries = beneficiaries[0] if beneficiaries else 'N/A'

#             return {
#                 "status": "success",
#                 "user": user,
#                 "accounts": accounts,
#                 "cards": cards,
#                 "beneficiaries": beneficiaries
#             }

#     except Exception as e:
#         return {"status": "error", "message": str(e)}
#     finally:
#         close_connection(connection)

# # Function to present banking options after successful login
# def after_login_option(registration):
#     registration.update_cell(5, 1, "Choose from the below banking options")
#     registration.update_cell(6, 1, "Type 1 in B5 cell to get user details")
#     registration.update_cell(7, 1, "Type 2 in B5 cell to get account information")
#     registration.update_cell(8, 1, "Type 3 in B5 cell to get card details")
#     registration.update_cell(9, 1, "Type 4 in B5 cell to get beneficiary details")
#     registration.update_cell(10, 1, "Type 5 in B5 cell to add new beneficiary details")
#     registration.update_cell(11, 1, "Type 6 in B5 cell to transfer funds")
#     registration.update_cell(12, 1, "Type anything in B5 cell to exit")
#     registration.update_cell(5, 2, "____________________________")
#     registration.update_cell(13, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")

# # Function to handle the main workflow based on user's selection
# def main_workflow(registration, option, result):
#     if option == '1':
#         update_cells_empty(registration, 5, 11, 1, 2)
#         data = result["user"]
#         registration.update_cell(5, 1, "username")
#         registration.update_cell(5, 2, data["username"])
#         registration.update_cell(6, 1, "full_name")
#         registration.update_cell(6, 2, data["full_name"])
#         registration.update_cell(7, 1, "address")
#         registration.update_cell(7, 2, data["address"])
#         registration.update_cell(8, 1, "aadhar")
#         registration.update_cell(8, 2, data["aadhar"])
#         registration.update_cell(9, 1, "mobile_no")
#         registration.update_cell(9, 2, data["mobile_no"])
#         registration.update_cell(10, 1, "email")
#         registration.update_cell(10, 2, data["email"])
#         registration.update_cell(11, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
        
       

         
        
#     elif option == '2':
#         get_account_info(registration, result)
#     elif option == '3':
#         get_card_details(registration, result)
#     elif option == '4':
#         get_beneficiary_details(registration, result)
#     elif option == '5':
#         add_new_beneficiary(registration, result)
#     elif option == '6':
#         handle_fund_transfer_prompt(registration)
#     else:
#         update_cells_empty(registration, 5, 11, 1, 2)
#         registration.update_cell(5, 3, "exit successfully")
#         return "Exit"

# # Function to handle the process of transferring funds
# def process_transfer_workflow(registration):
#     from_account_number = registration.get_cell(5, 2).value
#     to_account_number = registration.get_cell(6, 2).value
#     amount = registration.get_cell(7, 2).value
#     process_fund_transfer(registration, from_account_number, to_account_number, amount)

# # Main function to start the banking application
# def main():
#     registration = ...  # Obtain the registration object
#     option = registration.get_cell(5, 1).value
#     username = registration.get_cell(5, 2).value
#     password = registration.get_cell(6, 2).value

#     if option == 'login':
#         result = customer_login(username, password)
#         if result["status"] == "success":
#             after_login_option(registration)
#             option = registration.get_cell(5, 1).value
#             main_workflow(registration, option, result)
#         else:
#             registration.update_cell(5, 1, "Error: " + result["message"])
#     elif option == '6':
#         process_transfer_workflow(registration)
#     else:
#         registration.update_cell(5, 1, "Invalid option")

# if __name__ == "__main__":
#     main()
