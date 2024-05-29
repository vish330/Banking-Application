# main.py
from gsheet_connect import authenticate
from new_user_sheet import prompt_new_user_details, get_new_user_details, data_validation
from existing_user_sheet import customer_login, prompt_existing_user_details, after_login_option, user_datails
import gspread
from additional_function import wait_until_condition, check_condition, update_cells_empty
from user_input_functions import populate_database, populate_beneficiary_database
from beneficiary_sheet import prompt_beneficiary_input, get_beneficiary_input, beneficiary_data_validation

def main():
    gc = authenticate()
    # Open the workbook by name
    workbook = gc.open('Banking_System_UI')
    try:
        # Get the desired worksheet
        registration = workbook.worksheet('registration')  # pass the sheet name containing URL's

        registration.update_cell(1, 4, "Waiting")

        while registration.get_all_values()[0][3] == "Waiting":
            print('code start')

            if registration.get_all_values()[0][3] == "break":
                return

            # to empty up the screen before showing options to navigate 
            update_cells_empty(registration, 5, 15, 1, 3)

            registration.update_cell(3, 2, "Choose an option from the left drop down")
            registration.update_cell(4, 2, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue")

            print('waiting for users input')

            wait_until_condition(lambda: check_condition(registration))

            select_option = registration.get_all_values()[2][0]

            if select_option == "New Registration":

                registration.update_cell(1, 4, "Waiting")

                # showing the user the details required for a new registration
                prompt_new_user_details(registration)

                # pause condition for user to select and submit details 
                wait_until_condition(lambda: check_condition(registration))

                while True:
                    wait_until_condition(lambda: check_condition(registration))
                    registration.update_cell(1, 4, "Waiting")
                    user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type = get_new_user_details(registration)
                    invalid_count = data_validation(registration, user_name, password, full_name, address, aadhar, mobile_no, email, account_type, card_type)
                    if invalid_count == 0:
                        user_data = {"user_name": user_name, "password": password, "full_name": full_name, "address": address,
                                     "aadhar": aadhar, "mobile_no": mobile_no, "email": email, "account_type": account_type,
                                     "card_type": card_type}

                        populate_database(user_data)
                        registration.update_cell(5, 4, "Registration successful!")
                        update_cells_empty(registration, 5, 15, 1, 3)
                        registration.update_cell(1, 4, "Waiting")
                        break
                return

            elif select_option == "Login to your account":
                print("Existing customer")

                # Set the Google Sheet to "Waiting" while prompting existing user details
                registration.update_cell(1, 4, "Waiting")

                prompt_existing_user_details(registration)

                # Wait until user submits details
                wait_until_condition(lambda: check_condition(registration))

                registration.update_cell(1, 4, "Waiting")

                # Retrieve the user details from the Google Sheet
                user_name = registration.get_all_values()[4][1]
                password = registration.get_all_values()[5][1]

                # Authenticate the user with customer_login
                result = customer_login(user_name, password)
                print("Details fetched")

                if result["status"] == "success":
                    # announce successful login and clear specific cells 
                    registration.update_cell(5, 4, "Login successful!")
                    update_cells_empty(registration, 5, 15, 1, 3)
                    registration.update_cell(1, 4, "Waiting")

                    # Loop for user interaction after login
                    after_login_option(registration)

                    wait_until_condition(lambda: check_condition(registration))
                    registration.update_cell(1, 4, "Waiting")

                    # Get the choice from the Google Sheet
                    choice = registration.get_all_values()[4][1]
                    update_cells_empty(registration, 5, 15, 1, 3)

                    # logic for adding a new beneficiary
                    if choice == "5":
                        prompt_beneficiary_input(registration)
                        while True:
                            wait_until_condition(lambda: check_condition(registration))
                            registration.update_cell(1, 4, "Waiting")
                            beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc = get_beneficiary_input(registration)
                            invalid_count = beneficiary_data_validation(registration, beneficiary_name, beneficiary_account_number, beneficiary_bank, beneficiary_ifsc)
                            if invalid_count == 0:
                                account_id = result["accounts"]["account_id"]
                                user_data = {"beneficiary_name": beneficiary_name, "beneficiary_account_number": beneficiary_account_number, "beneficiary_bank": beneficiary_bank, "beneficiary_ifsc": beneficiary_ifsc}
                                populate_beneficiary_database(user_data, account_id)
                                registration.update_cell(5, 4, "Beneficiary added successful!")
                                registration.update_cell(1, 4, "Waiting")
                                update_cells_empty(registration, 5, 15, 1, 3)
                                break

                    else:
                        details_user = user_datails(registration, choice, result)  # Handle user details and selected option

                        if details_user == "Exit":
                            registration.update_cell(1, 4, "Submit Details")
                            update_cells_empty(registration, 5, 15, 1, 3)
                        else:
                            print("Continuing the loop")
                            registration.update_cell(5, 4, "Click on submit_details to continue banking.")
                            wait_until_condition(lambda: check_condition(registration))
                            update_cells_empty(registration, 5, 15, 1, 3)

                else:
                    # If login fails, update the Google Sheet with an error message
                    registration.update_cell(5, 3, "Invalid username or password")
                    registration.update_cell(1, 4, "Waiting")
                    return  # Exit if login fails

            else:
                registration.update_cell(3, 2, "Please select and option to continue")
                registration.update_cell(1, 4, "Waiting")

    except gspread.exceptions.APIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


