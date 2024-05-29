import re

# Function to prompt beneficiary details
def prompt_beneficiary_input(registration):
    print("inside get_beneficiary_input")

    registration.update_cell(5,1,"Enter beneficiary name")
    registration.update_cell(6,1,"Enter beneficiary account number")
    registration.update_cell(7,1,"Enter beneficiary bank name")
    registration.update_cell(8,1,"Enter beneficiary IFSC code")
    registration.update_cell(9,1,"Click on SUBMIT DETAILS from the drop down in D1 cell.")
    print("outside get_beneficiary_input")

    return 

# Function to read beneficiary details 
def get_beneficiary_input(registration):
   print("inside get_beneficiary_input")
   global beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc

   beneficiary_name = registration.get_all_values()[4][1]
   beneficiary_account_number = registration.get_all_values()[5][1]
   beneficiary_bank = registration.get_all_values()[6][1].lower()
   beneficiary_ifsc = registration.get_all_values()[7][1]

   print("outside get_beneficiary_input")
   return beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc

# Function to validate the beneficiary details
def beneficiary_data_validation(registration, beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc):
    
    registration.update_cell(1,4,"Waiting")

    invalid_count = 0
    
    if not re.match(r"^[a-zA-Z\s]+$", beneficiary_name):
        invalid_count+=1
        registration.update_cell(5,3,"Beneficiary name must contain only alphabetic characters and spaces.")
    else:
        registration.update_cell(5,3,"valid beneficiary name")

    if not re.match(r"^\d{10,20}$", beneficiary_account_number):
        invalid_count+=1
        registration.update_cell(6,3,"Beneficiary account number must be a number between 10 and 20 digits.")
    else:
        registration.update_cell(6,3,"valid beneficiary account number")

    if not re.match(r"^[a-zA-Z\s]+$", beneficiary_bank):
        invalid_count+=1
        registration.update_cell(7,3,"Beneficiary bank name must contain only alphabetic characters and spaces.")
    else:
        registration.update_cell(7,3,"valid beneficiary bank")

    if not re.match(r"^[A-Z0-9]{11}$", beneficiary_ifsc):
        invalid_count+=1
        registration.update_cell(8,3,"Beneficiary IFSC code must be 11 characters long, containing only uppercase letters and numbers.")
    else:
        registration.update_cell(8,3,"valid beneficiary ifsc")

    return invalid_count
