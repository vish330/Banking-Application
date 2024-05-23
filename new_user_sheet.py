import re

def prompt_new_user_details():
    print("inside prompt_new_user_details")
    
    user_details = {}
    user_details["user_name"] = input("Enter Username: ")
    user_details["password"] = input("Enter Your Password: ")
    user_details["full_name"] = input("Enter Your Full Name: ")
    user_details["address"] = input("Enter Address: ")
    user_details["aadhar"] = input("Enter Aadhar Number: ")
    user_details["mobile_no"] = input("Enter Mobile Number: ")
    user_details["email"] = input("Enter Email Address: ")
    user_details["account_type"] = input("Enter account type (savings/current): ").lower()
    user_details["card_type"] = input("Enter card type (credit/debit): ").lower()
    
    print("outside prompt_new_user_details")
    return user_details


def get_new_user_details(user_details):
    print("inside get_new_user_details")

    user_name = user_details["user_name"]
    password = user_details["password"]
    full_name = user_details["full_name"]
    address = user_details["address"]
    aadhar = user_details["aadhar"]
    mobile_no = user_details["mobile_no"]
    email = user_details["email"]
    account_type = user_details["account_type"]
    card_type = user_details["card_type"]
    
    print("outside get_new_user_details")
    return user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type


def data_validation(user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type):
    print("inside data_validation")
    
    invalid_count = 0

    if not re.match(r"^[a-zA-Z\s_]+$", user_name):
        invalid_count += 1
        print("Username must contain only alphabetic characters, spaces, or underscores.")
    else:
        print("Valid username")
    
    if not re.match(r"^(?=.*[!@#$%^&*()_+}{\":;'?/>.<,])(?=.*[A-Z])(?=.*[a-z]).{8,}$", password):
        invalid_count += 1
        print("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one special character")
    else:
        print("Valid password")
    
    if not re.match(r"^[a-zA-Z\s]+$", full_name):
        invalid_count += 1
        print("Full name must contain only alphabetic characters and spaces.")
    else:
        print("Valid full name")
    
    if not address:
        invalid_count += 1
        print("Address can't be empty.")
    else:
        print("Valid address")
    
    if not re.match(r"^\d{14}$", aadhar):
        invalid_count += 1
        print("Aadhar must contain exactly 14 digits.")
    else:
        print("Valid aadhar")
    
    if not re.match(r"^\d{10}$", mobile_no):
        invalid_count += 1
        print("Mobile number must contain exactly 10 digits.")
    else:
        print("Valid mobile number")
    
    if not email.endswith("@gmail.com"):
        invalid_count += 1
        print("Email must end with '@gmail.com'.")
    else:
        print("Valid email")
    
    if account_type not in ['savings', 'current']:
        invalid_count += 1
        print("Account type should be either savings or current.")
    else:
        print("Valid account type")
    
    if card_type not in ['credit', 'debit']:
        invalid_count += 1
        print("Card type should be either credit or debit.")
    else:
        print("Valid card type")
    
    print("outside data_validation")
    
    return invalid_count


if __name__ == "__main__":
    user_details = prompt_new_user_details()
    user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type = get_new_user_details(user_details)
    invalid_count = data_validation(user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type)
    
    if invalid_count == 0:
        print("All user details are valid.")
    else:
        print(f"Total invalid fields: {invalid_count}")
