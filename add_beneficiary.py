def add_new_beneficiary(registration, result):
    # Placeholder function to handle adding new beneficiary details
    # Implement the logic to prompt user for new beneficiary details and save them to the database
    registration.update_cell(5, 1, "Enter new beneficiary details")
    registration.update_cell(6, 1, "Beneficiary Name:")
    registration.update_cell(7, 1, "Beneficiary Account Number:")
    registration.update_cell(8, 1, "Beneficiary Bank:")
    registration.update_cell(9, 1, "Beneficiary IFSC:")
    registration.update_cell(10, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell.")
