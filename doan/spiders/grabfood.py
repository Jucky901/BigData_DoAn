import pandas as pd

# Read the CSV file
df = pd.read_csv('pandastore.csv')

# Strip whitespace from column names to avoid key errors
df.columns = df.columns.str.strip()

# Print columns to verify structure
print("Columns:", df.columns)

# Define the function to adjust ratings
def adjust_rating(value):
    try:
        # Attempt to convert to float
        float_value = float(value)
        # Convert to string excluding the decimal point
        value_str = str(value).replace('.', '')
        # Check length
        if len(value_str) >= 3:
            return 0
        return float_value
    except ValueError:
        # If conversion fails, set to 0
        return 0

# Apply the function to the 'rating' column
if 'rating' in df.columns:
    df['rating'] = df['rating'].apply(adjust_rating)
else:
    print("Error: 'rating' column not found")

# Save the cleaned data
df.to_csv('pandas.csv', index=False)

print("Data processed and saved to pandas.csv")
