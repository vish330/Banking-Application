from additional_function import update_cells_empty

def get_user_details(registration, result):
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
