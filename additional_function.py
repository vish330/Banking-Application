import time
from gsheet_connect import authenticate


def wait_until_condition(condition_func):
    while not condition_func():
        print("Condition not satisfied, waiting for 10 seconds...")
        time.sleep(10)
    print("Condition satisfied!")

def check_condition(registration):
    if registration.get_all_values()[0][3] == "Waiting":
        return False
    else:
        return True
    

def update_cells_empty(worksheet, start_row, end_row, start_column, end_column):
    print("inside update_cells_empty")
    for row in range(start_row, end_row + 1):
        for col in range(start_column, end_column + 1):
            worksheet.update_cell(row, col, "")
    print("outside update_cells_empty")
