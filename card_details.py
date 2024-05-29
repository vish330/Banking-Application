from additional_function import update_cells_empty

def get_card_details(registration, result):
    data = result["cards"]
    update_cells_empty(registration, 5, 11, 1, 2)
    if data == 'N/A':
        registration.update_cell(5, 1, "No details found")
        return

    registration.update_cell(5, 1, "card_number")
    card_number = str(int(float(data["card_number"])))
    registration.update_cell(5, 2, card_number)
    registration.update_cell(6, 1, "card_type")
    registration.update_cell(6, 2, data["card_type"])
    registration.update_cell(7, 1, "cvv")
    registration.update_cell(7, 2, data["cvv"])
    registration.update_cell(8, 1, "expiry_date")
    expiry_date_str = data["expiry_date"].strftime("%Y-%m-%d")
    registration.update_cell(8, 2, expiry_date_str)
    registration.update_cell(9, 1, "mpin")
    registration.update_cell(9, 2, data["mpin"])
    registration.update_cell(10, 1, "Click on SUBMIT DETAILS from the drop down in D1 cell to continue.")
