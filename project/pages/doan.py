import subprocess
import streamlit as st
import pandas as pd
from io import StringIO

def run_sqoop_eval(query):
    command = [
        "sqoop", "eval",
        "--connect", "jdbc:mysql://localhost/QuanLyQuanAn",
        "--username", "sqoopdb",
        "--password", "Abc123456!@#",
        "--query", query
    ]
    
    try:
        # Redirect stderr to subprocess.PIPE to capture warnings
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Only return stdout (the actual result), ignoring stderr (warnings)
        return result.stdout

    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def parse_sqoop_output(output):
    # Split the output by lines
    lines = output.split("\n")
    
    # Skip the first two lines (which are headers and empty lines)
    cleaned_lines = lines[2:]  # Skip the first 2 lines (header and empty lines)
    
    # Remove any completely empty lines
    cleaned_lines = [line for line in cleaned_lines if line.strip()]
    
    # Remove the first line (the row containing '0') from the cleaned lines
    if cleaned_lines:
        cleaned_lines = cleaned_lines[1:]
    
    # Split the rows by '|' and clean the data
    data = [line.split("|")[1:-1] for line in cleaned_lines]  # Skip the first and last empty fields
    
    header_values = ['tenquan', 'id','rating', 'item', 'price']
    cleaned_data = []
    for row in data:
        cleaned_row = [cell.strip() for cell in row]
        # Check if the row contains any valid data (i.e., no empty strings)
        if any(cell != '' for cell in cleaned_row) and cleaned_row != header_values:
            cleaned_data.append(cleaned_row)
    
    # Define the column names
    columns = ["Restaurant Name", "Id" ,"Rating", "Item", "Price"]
    
    # Create DataFrame
    df = pd.DataFrame(cleaned_data, columns=columns)
    
    # Reset the index and drop the default index column
    df = df.reset_index(drop=True)
    
    for idx, row in df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 2, 1, 1, 1])

        with col1:
            st.write(row["Restaurant Name"])
        with col2:
            st.write(row["Id"])
        with col3:
            st.write(row["Rating"])
        with col4:
            st.write(row["Item"])
        with col5:
            st.write(row["Price"])
        with col6:
            if st.button("Delete", key=f"delete_{idx}"):
                query = f"Delete From DOAN where idquan = {row['Id']} and item = '{row['Item']}';"
                out = run_sqoop_eval(query)
                st.rerun()
    return df

# Streamlit user interface
st.title("Đồ ăn")

# Separate search bars for Restaurant Name and Address
search_tenquan = st.text_input("Search by Restaurant Name", "")
search_tendoan = st.text_input("Search by Food Name", "")

# Add a combo box to select rating
rating = st.selectbox("Select Rating", ["All", 1, 2, 3, 4, 5], index=0)
price = st.selectbox("Select Price", ["All", "Tu 50k tro xuong", "Tu 50k den 100k", "Tu 100k den 200k", "Tu 200k den 500k, Tu 500k tro len"], index=0)
sort = st.selectbox("Sort", ["Sort","Sort by Restaurant Name DESC", "Sort by Restaurant Name ASC", "Sort by Item DESC", "Sort by Item ASC", "Sort by Price DESC", "Sort by Price ASC"], index=0)
# Default query
query = "Select tenquan, id ,DOAN.rating, item, price  From DOAN left join QUANAN on DOAN.idquan = QUANAN.id"

# Create a list to store conditions
conditions = []

# Track if the filter is changed (for resetting the page)
filters_changed = False

# Scenario 1: Search by Restaurant Name  (tenquan)
if search_tendoan:
    conditions.append(f"item LIKE '%{search_tendoan}%'")
    filters_changed = True

if search_tenquan:
    conditions.append(f"tenquan LIKE '%{search_tenquan}%'")
    filters_changed = True

# Scenario 3: Filter by Rating 
if rating != "All":
    conditions.append(f"DOAN.rating >= {rating} AND DOAN.rating < {rating + 1}")
    filters_changed = True

#Scenario 4: Filter by Sort

if price != "All":
    if price == "Tu 50k tro xuong":
        conditions.append("price <= 50000")
    elif price == "Tu 50k den 100k":
        conditions.append("price >= 50000 AND price <= 100000")
    elif price == "Tu 100k den 200k":
        conditions.append("price >= 100000 AND price <= 200000")
    elif price == "Tu 200k den 500k":
        conditions.append("price >= 200000 AND price <= 500000")
    elif price == "Tu 500k tro len":
        conditions.append("price >= 500000")

# Sorting Logic
if sort != "Sort":
    if sort == "Sort by Restaurant Name DESC":
        sort_query = "ORDER BY tenquan DESC"
    elif sort == "Sort by Restaurant Name ASC":
        sort_query = "ORDER BY tenquan ASC"
    elif sort == "Sort by Item DESC":
        sort_query = "ORDER BY item DESC"
    elif sort == "Sort by Item ASC":
        sort_query = "ORDER BY item ASC"
    elif sort == "Sort by Price DESC":
        sort_query = "ORDER BY price DESC"
    elif sort == "Sort by Price ASC":
        sort_query = "ORDER BY price ASC"
    filters_changed = True
else:
    sort_query = ""


# Combine conditions with 'AND' if there are any conditions
if conditions:
    query += " WHERE " + " AND ".join(conditions)
query += f" {sort_query}"
# Reset the page to the first page when filters change
if filters_changed:
    st.session_state.page = 0

# Run Sqoop Eval command
output = run_sqoop_eval(query)


# Parse the output into a DataFrame
if "Error" not in output:
    parse_sqoop_output(output)
else:
    st.error(output)

