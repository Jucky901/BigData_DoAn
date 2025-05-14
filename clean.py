import pandas as pd

df = pd.read_csv('grabstore1.csv')


df.columns = df.columns.str.strip()
df_cleaned = df.drop_duplicates()

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

if 'rating' in df.columns:
    df['rating'] = df['rating'].apply(adjust_rating)
else:
    print("Error: 'rating' column not found")

# Save the cleaned data
df.to_csv('grabstore1w.csv', index=False)

print("Data processed and saved to pandas.csv")
