# HTTP Error 403: Forbidden

import pandas as pd

# used the 'Existing Access' version of the link
sharepoint_path = 'https://nhs.sharepoint.com/:f:/r/sites/msteams_4e25bd-ValuePackProduction/Shared%20Documents/Value%20Pack%20Production/Data?csf=1&web=1&e=kiqQQu'

worksheet = 'Sheet1'

import_df = pd.read_excel(sharepoint_path,sheet_name=worksheet)

print(import_df)

