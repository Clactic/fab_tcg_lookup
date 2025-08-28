import justtcg.helpers
import data.data_converter as data_converter
import pandas as pd
from openpyxl.styles import Font, PatternFill
import os
from google_docs.formatter import format_sheet

################ MY COLLECTION PRICE TRACKER ################
my_collection = data_converter.convert_csv_to_dict('data/my_collection.csv')

# Batch request in chunks of 20
my_collection_responses = []
for batch in justtcg.helpers.chunk_list(my_collection, 20):
    resp = justtcg.helpers.track_collection_prices(batch)
    my_collection_responses.extend(resp)

# Convert my_collection.csv to a DataFrame
my_collection_df = pd.read_csv('data/my_collection.csv')

# Convert response to DataFrame
my_collection_response_df = pd.DataFrame(my_collection_responses)

# Ensure both columns are string type
my_collection_response_df['tcgplayerid'] = my_collection_response_df['tcgplayerid'].astype(str)
my_collection_response_df['printing'] = my_collection_response_df['printing'].astype(str)
my_collection_df['TCGPlayerId'] = my_collection_df['TCGPlayerId'].astype(str)
my_collection_df['Printing'] = my_collection_df['Printing'].astype(str)

# Merge on tcgplayerid and printing
my_collection_merged_df = my_collection_response_df.merge(
    my_collection_df[['TCGPlayerId', 'Printing', 'Quanity']], 
    left_on=['tcgplayerid', 'printing'], 
    right_on=['TCGPlayerId', 'Printing'], 
    how='left'
)

# Optionally rename 'Quanity' to 'quantity'
my_collection_merged_df = my_collection_merged_df.rename(columns={'Quanity': 'quantity'})

# Reorder columns
my_collection_merged_df = my_collection_merged_df[
    ['tcgplayerid', 'quantity', 'cardid', 'set', 'name', 'rarity', 'printing', 'current_price', 'price_delta_7d(%)', 'last_updated']
]

# Convert last_updated from Unix timestamp to date string
my_collection_merged_df['last_updated'] = pd.to_datetime(my_collection_merged_df['last_updated'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

# Save to CSV
my_collection_merged_df.to_csv('data/updated_file.csv', index=False)

########################Looking For Price Tracker########################
looking_for = data_converter.convert_csv_to_dict('data/looking_for.csv')

# Batch request in chunks of 20
looking_for_responses = []
for batch in justtcg.helpers.chunk_list(looking_for, 20):
    resp = justtcg.helpers.track_collection_prices(batch)
    looking_for_responses.extend(resp)

# Convert response to DataFrame
looking_for_response_df = pd.DataFrame(looking_for_responses)
looking_for_df = pd.read_csv('data/looking_for.csv')

# Ensure both columns are string type
looking_for_response_df['tcgplayerid'] = looking_for_response_df['tcgplayerid'].astype(str)
looking_for_response_df['printing'] = looking_for_response_df['printing'].astype(str)
looking_for_df['TCGPlayerId'] = looking_for_df['TCGPlayerId'].astype(str)
looking_for_df['Printing'] = looking_for_df['Printing'].astype(str)

# Merge on tcgplayerid and printing
looking_for_merged_df = looking_for_response_df.merge(
    looking_for_df[['TCGPlayerId', 'Printing', 'Quanity']], 
    left_on=['tcgplayerid', 'printing'], 
    right_on=['TCGPlayerId', 'Printing'], 
    how='left'
)

# Optionally rename 'Quanity' to 'quantity'
looking_for_merged_df = looking_for_merged_df.rename(columns={'Quanity': 'quantity'})

# Reorder columns
looking_for_merged_df = looking_for_merged_df[
    ['tcgplayerid', 'quantity', 'cardid', 'set', 'name', 'rarity', 'printing', 'current_price', 'price_delta_7d(%)', 'last_updated']
]

# Convert last_updated from Unix timestamp to date string
looking_for_merged_df['last_updated'] = pd.to_datetime(looking_for_merged_df['last_updated'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

# Save to CSV
looking_for_merged_df.to_csv('data/looking_for_updated_file.csv', index=False)

# Sort DataFrames before writing to Excel
my_collection_merged_df = my_collection_merged_df.sort_values(['set', 'cardid'])
looking_for_merged_df = looking_for_merged_df.sort_values(['set', 'cardid'])

# Write both DataFrames to separate sheets in one Excel file and format
with pd.ExcelWriter('data/trade_and_wantlist.xlsx', engine='openpyxl') as writer:
    my_collection_merged_df.to_excel(writer, sheet_name='Looking_To_Trade', index=False)
    looking_for_merged_df.to_excel(writer, sheet_name='Looking_For', index=False)
    workbook = writer.book
    for sheet_name in ['Looking_To_Trade', 'Looking_For']:
        worksheet = workbook[sheet_name]
        format_sheet(worksheet)

# Remove temporary CSV files
os.remove('data/updated_file.csv')
os.remove('data/looking_for_updated_file.csv')

print('finished')