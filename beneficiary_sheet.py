import re

def prompt_beneficiary_input():
    print("inside prompt_beneficiary_input")
    
    beneficiary_details = {}
    beneficiary_details["beneficiary_name"] = input("Enter beneficiary name: ")
    beneficiary_details["beneficiary_account_number"] = input("Enter beneficiary account number: ")
    beneficiary_details["beneficiary_bank"] = input("Enter beneficiary bank name: ").lower()
    beneficiary_details["beneficiary_ifsc"] = input("Enter beneficiary IFSC code: ")
    
    print("outside prompt_beneficiary_input")
    return beneficiary_details


def get_beneficiary_input(beneficiary_details):
    print("inside get_beneficiary_input")
    
    beneficiary_name = beneficiary_details["beneficiary_name"]
    beneficiary_account_number = beneficiary_details["beneficiary_account_number"]
    beneficiary_bank = beneficiary_details["beneficiary_bank"]
    beneficiary_ifsc = beneficiary_details["beneficiary_ifsc"]
    
    print("outside get_beneficiary_input")
    return beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc


def beneficiary_data_validation(beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc):
    print("inside beneficiary_data_validation")
    
    invalid_count = 0
    
    if not re.match(r"^[a-zA-Z\s]+$", beneficiary_name):
        invalid_count += 1
        print("Beneficiary name must contain only alphabetic characters and spaces.")
    else:
        print("Valid beneficiary name")
    
    if not re.match(r"^\d{10,20}$", beneficiary_account_number):
        invalid_count += 1
        print("Beneficiary account number must be a number between 10 and 20 digits.")
    else:
        print("Valid beneficiary account number")
    
    if not re.match(r"^[a-zA-Z\s]+$", beneficiary_bank):
        invalid_count += 1
        print("Beneficiary bank name must contain only alphabetic characters and spaces.")
    else:
        print("Valid beneficiary bank")
    
    if not re.match(r"^[A-Z0-9]{11}$", beneficiary_ifsc):
        invalid_count += 1
        print("Beneficiary IFSC code must be 11 characters long, containing only uppercase letters and numbers.")
    else:
        print("Valid beneficiary IFSC")
    
    print("outside beneficiary_data_validation")
    return invalid_count


if __name__ == "__main__":
    beneficiary_details = prompt_beneficiary_input()
    beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc = get_beneficiary_input(beneficiary_details)
    invalid_count = beneficiary_data_validation(beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc)
    
    if invalid_count == 0:
        print("All beneficiary details are valid.")
    else:
        print(f"Total invalid fields: {invalid_count}")

