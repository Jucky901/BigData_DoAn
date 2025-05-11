import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('store.csv')

# Remove duplicate rows based on all columns
df_cleaned = df.drop_duplicates()

# Optionally, you can specify certain columns to check for duplicates
# df_cleaned = df.drop_duplicates(subset=['column1', 'column2'])

# Write the cleaned DataFrame back to a new CSV file
df_cleaned.to_csv('cleanedStore.csv', index=False)

print("Duplicates removed and saved")
