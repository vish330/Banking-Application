# user_input_functions
import hashlib
from mysql_connection import get_connection, close_connection


# Function to insert data into the Users table
def insert_user(cursor, user_data):
   # Hash the raw password for security
   hashed_password = hashlib.sha256(user_data["password"].encode()).hexdigest()

   sql = """
   INSERT INTO Users (username, password, full_name, address, aadhar, mobile_no, email)
   VALUES (%s, %s, %s, %s, %s, %s, %s)
   """
  
   data = (
       user_data["user_name"],
       hashed_password,
       user_data["full_name"],
       user_data["address"],
       user_data["aadhar"],
       user_data["mobile_no"],
       user_data["email"],
   )

   cursor.execute(sql, data)
   return cursor.lastrowid  # Return the ID of the new user





def insert_account(cursor, account_data, user_id):
  
    sql = """
    INSERT INTO Accounts (user_id, account_type, balance)
    VALUES (%s, %s, %s)
    """
    
    data = (user_id, account_data["account_type"], 5000.00)
    
    cursor.execute(sql, data)

    
    account_id = cursor.lastrowid

  
    account_id_str = str(account_id).zfill(11)

    return account_id_str






# Function to insert data into the Cards table
def insert_card(cursor, card_data, account_id):
   sql = """
   INSERT INTO Cards (account_id, card_type)
   VALUES (%s, %s)
   """
  
   data = (account_id, card_data["card_type"])
   cursor.execute(sql, data)
   return cursor.lastrowid  # Return the ID of the new card


def populate_database(data):
    print("inside populate_database")
    connection = get_connection()  # Establish database connection

    if connection is not None:
        try:
            cursor = connection.cursor()  # Create a cursor to execute queries

            # Begin transaction
            cursor.execute("START TRANSACTION")

            # Get user input and insert into Users table
            user_input = data
            user_id = insert_user(cursor, user_input)

            # Get account input and insert into Accounts table
            account_input = data
            account_id = insert_account(cursor, account_input, user_id)

            # Get card input and insert into Cards table
            card_input = data
            card_id = insert_card(cursor, card_input, account_id)

            # Commit the transaction to save all changes
            connection.commit()

            print("All data inserted successfully.")

            print("outside populate_database")
        except Exception as e:
            # Roll back the transaction in case of errors
            connection.rollback()
            print("An error occurred:", e)

        finally:
            # Use close_connection to clean up
            close_connection(connection, cursor)

# # Get beneficiary input and insert into Beneficiaries table
# beneficiary_input = get_beneficiary_input()
# beneficiary_id = insert_beneficiary(cursor, beneficiary_input, account_id)



# Function to insert data into the Beneficiaries table
def insert_beneficiary(cursor, beneficiary_data, account_id):
   sql = """
   INSERT INTO Beneficiaries (account_id, beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc)
   VALUES (%s, %s, %s, %s, %s)
   """
  
   data = (
       account_id,
       beneficiary_data["beneficiary_name"],
       beneficiary_data["beneficiary_account_number"],
       beneficiary_data["beneficiary_bank"],
       beneficiary_data["beneficiary_ifsc"]
   )

   cursor.execute(sql, data)
   return cursor.lastrowid  # Return the ID of the new beneficiary

def populate_beneficiary_database(data, account_id):
    print("inside populate_beneficiary_database")
    connection = get_connection()  # Establish database connection

    if connection is not None:
        try:
            cursor = connection.cursor()  # Create a cursor to execute queries

            # Begin transaction
            cursor.execute("START TRANSACTION")

            # Get card input and insert into Cards table
            beneficiary_input = data
            beneficiary_id = insert_beneficiary(cursor, beneficiary_input, account_id)

            # Commit the transaction to save all changes
            connection.commit()

            print("All data inserted successfully.")

            print("outside populate_beneficiary_database")
        
        except Exception as e:
            # Roll back the transaction in case of errors
            connection.rollback()
            print("An error occurred:", e)

        finally:
            # Use close_connection to clean up
            close_connection(connection, cursor)
