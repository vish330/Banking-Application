from additional_function import update_cells_empty

def get_account_info(registration, result):
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
