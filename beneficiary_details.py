from additional_function import update_cells_empty

def get_beneficiary_details(registration, result):
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
