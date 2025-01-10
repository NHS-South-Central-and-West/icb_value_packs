import pandas as pd

def extract_data(worksheet,first,last): #i.e. reference for first cell and last cell in table 
    data_rows = []

    for row in worksheet[first:last]:
        data_cols = []
        for cell in row:
            data_cols.append(cell.value)
        data_rows.append(data_cols)
    df = pd.DataFrame(data_rows)
    return df