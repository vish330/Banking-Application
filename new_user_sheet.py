#new_user_sheet
import re

# Function to show prompts for new user registration
def prompt_new_user_details(registration):
   print("inside prompt_new_user_details")

   registration.update_cell(5,1,"Enter Username: ")
   registration.update_cell(6,1,"Enter Your Password: ")
   registration.update_cell(7,1,"Enter Your Full Name: ")
   registration.update_cell(8,1,"Enter Address: ")
   registration.update_cell(9,1,"Enter Aadhar Number: ")
   registration.update_cell(10,1,"Enter Mobile Number: ")
   registration.update_cell(11,1,"Enter Email Address: ")
   registration.update_cell(12,1,"Enter account type (savings/current): ")
   registration.update_cell(13,1,"Enter card type (credit/debit): ")
   registration.update_cell(14,1,"Click on SUBMIT DETAILS from the drop down in D1 cell.")
   print("outside prompt_new_user_details")
   return

# Function to collect user details
def get_new_user_details(registration):
   print("inside get_new_user_details")
   global user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type

   user_name = registration.get_all_values()[4][1]
   password = registration.get_all_values()[5][1]
   full_name = registration.get_all_values()[6][1]
   address = registration.get_all_values()[7][1]
   aadhar = registration.get_all_values()[8][1]
   mobile_no = registration.get_all_values()[9][1]
   email = registration.get_all_values()[10][1]
   account_type = registration.get_all_values()[11][1].lower()
   card_type = registration.get_all_values()[12][1].lower()
   print("outside get_new_user_details")
   return user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type

def data_validation(registration, user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type):
    print("inside data_validation")
    registration.update_cell(1,4,"Waiting")
    
    invalid_count = 0

   # Validate user_name (alphabetic, spaces, underscores)
    if not re.match(r"^[a-zA-Z\s_]+$", user_name):
        invalid_count+=1
        registration.update_cell(5,3,"Username must contain only alphabetic characters, spaces, or underscores.")

    else:
        registration.update_cell(5,3,"Valid user name")

   # Validate password (criteria)
    if not re.match(r"^(?=.*[!@#$%^&*()_+}{\":;'?/>.<,])(?=.*[A-Z])(?=.*[a-z]).{8,}$", password):
        invalid_count+=1
        registration.update_cell(6,3,"Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character")
    else:
        registration.update_cell(6,3,"Valid password")

   # Validate full_name (alphabetic with spaces)
    if not re.match(r"^[a-zA-Z\s]+$", full_name):
        invalid_count+=1
        registration.update_cell(7,3,"Full name must contain only alphabetic characters and spaces.")
    
    else:
        registration.update_cell(7,3,"Valid full name")

   # address (should not be empty)
    if not address:
        invalid_count+=1
        registration.update_cell(8,3,"Address can't be empty.")
    else:
        registration.update_cell(8,3,"Valid address")

   # Validate aadhar (14 digits)
    if not re.match(r"^\d{14}$", aadhar):
        invalid_count+=1
        registration.update_cell(9,3,"Aadhar must contain exactly 14 digits.")

    else:
        registration.update_cell(9,3,"Valid aadhar")

   # Validate mobile_no (10 digits)
    if not re.match(r"^\d{10}$", mobile_no):
        invalid_count+=1
        registration.update_cell(10,3,"Mobile number must contain exactly 10 digits.")

    else:
        registration.update_cell(10,3,"Valid mobile no.")
   
   # Validate email ends with '@gmail.com'
    if not email.endswith("@gmail.com"):
       invalid_count+=1
       registration.update_cell(11,3,"Email must end with '@gmail.com'.")

    else:
        registration.update_cell(11,3,"Valid email")

   # Validate account_type 
    if account_type not in ['savings', 'current']:
       invalid_count+=1
       registration.update_cell(12,3,"account_type should be either savings or current.")
    else:
        registration.update_cell(12,3,"Valid account type")

   # Validate card_type 
    if card_type not in ['credit', 'debit']:
       invalid_count+=1
       registration.update_cell(13,3,"card_type should be either of credit or debit.")
    else:
        registration.update_cell(13,3,"Valid card type")
    
    print("outside data_validation")
    
    return invalid_count
