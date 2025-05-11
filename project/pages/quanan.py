import subprocess
import streamlit as st

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
    
    header_values = ['id', 'tenquan', 'diachi', 'rating']
    
    # Directly display each row with the corresponding data
    for row in data:
        cleaned_row = [cell.strip() for cell in row]
        
        # Check if the row contains any valid data (i.e., no empty strings)
        if any(cell != '' for cell in cleaned_row) and cleaned_row != header_values:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 1])

            with col1:
                st.write(cleaned_row[0])  # ID
            with col2:
                st.write(cleaned_row[1])  # Restaurant Name
            with col3:
                st.write(cleaned_row[2])  # Address
            with col4:
                st.write(cleaned_row[3])  # Rating
            with col5:
                if st.button("Delete", key=f"delete_{cleaned_row[0]}"):
                    query = f"DELETE FROM QUANAN WHERE id = {cleaned_row[0]};"
                    query2 = f"DELETE FROM DOAN WHERE id = {cleaned_row[0]};"
                    out = run_sqoop_eval(query2)
                    out = run_sqoop_eval(query1)
                    st.rerun()
    
# Streamlit user interface
st.title("Quan an")

# Separate search bars for Restaurant Name and Address
search_tenquan = st.text_input("Search by Restaurant Name", "")
search_diachi = st.text_input("Search by Address", "")

# Add a combo box to select rating
rating = st.selectbox("Select Rating", ["All", 1, 2, 3, 4, 5], index=0)
sort = st.selectbox("Sort", ["Sort","Sort by Restaurant Name DESC", "Sort by Restaurant Name ASC", "Sort by Address DESC", "Sort by Address ASC", "Sort by Rating DESC", "Sort by Rating ASC"], index=0)

# Default query
query = "SELECT * FROM QUANAN"

# Create a list to store conditions
conditions = []

# Track if the filter is changed (for resetting the page)
filters_changed = False

# Scenario 1: Search by Restaurant Name  (tenquan)
if search_tenquan:
    conditions.append(f"tenquan LIKE '%{search_tenquan}%'")
    filters_changed = True

# Scenario 2: Search by Address  (diachi)
if search_diachi:
    conditions.append(f"diachi LIKE '%{search_diachi}%'")
    filters_changed = True

# Scenario 3: Filter by Rating 
if rating != "All":
    conditions.append(f"rating >= {rating} AND rating < {rating + 1}")
    filters_changed = True

# Scenario 4: Filter by Sort
# Sorting Logic
if sort != "Sort":
    if sort == "Sort by Restaurant Name DESC":
        sort_query = "ORDER BY tenquan DESC"
    elif sort == "Sort by Restaurant Name ASC":
        sort_query = "ORDER BY tenquan ASC"
    elif sort == "Sort by Address DESC":
        sort_query = "ORDER BY diachi DESC"
    elif sort == "Sort by Address ASC":
        sort_query = "ORDER BY diachi ASC"
    elif sort == "Sort by Rating DESC":
        sort_query = "ORDER BY rating DESC"
    elif sort == "Sort by Rating ASC":
        sort_query = "ORDER BY rating ASC"
    filters_changed = True
else:
    sort_query = ""

# Combine conditions with 'AND' if there are any conditions
if conditions:
    query += " WHERE " + " AND ".join(conditions)
query += f" {sort_query}"

# Run Sqoop Eval command
output = run_sqoop_eval(query)

# Display the output directly in Streamlit
if "Error" not in output:
    parse_sqoop_output(output)
else:
    st.error(output)

