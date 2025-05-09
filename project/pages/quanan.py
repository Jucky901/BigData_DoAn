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
    
    header_values = ['id', 'tenquan', 'diachi', 'rating']
    cleaned_data = []
    for row in data:
        cleaned_row = [cell.strip() for cell in row]
        # Check if the row contains any valid data (i.e., no empty strings)
        if any(cell != '' for cell in cleaned_row) and cleaned_row != header_values:
            cleaned_data.append(cleaned_row)
    
    # Define the column names
    columns = ["ID", "Restaurant Name", "Address", "Rating"]
    
    # Create DataFrame
    df = pd.DataFrame(cleaned_data, columns=columns)
    
    # Reset the index and drop the default index column
    df = df.reset_index(drop=True)
    
    return df

# Streamlit user interface
st.title("Quan an")

# Separate search bars for Restaurant Name and Address
search_tenquan = st.text_input("Search by Restaurant Name", "")
search_diachi = st.text_input("Search by Address", "")

# Add a combo box to select rating
rating = st.selectbox("Select Rating", ["All", 1, 2, 3, 4, 5], index=0)
sort = st.selectbox("Sort", ["Sort","Sort by Restaurant Name DESC", "Sort by Restaurant Name ASC", "Sort by Address DESC", "Sort by Address ASC", "Sort by Address DESC", "Sort by Address ASC"], index=0)
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

#Scenario 4: Filter by Sort
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
# Reset the page to the first page when filters change
if filters_changed:
    st.session_state.page = 0

# Run Sqoop Eval command
output = run_sqoop_eval(query)


# Parse the output into a DataFrame
if "Error" not in output:
    df = parse_sqoop_output(output)

    # Define the number of rows per page
    rows_per_page = 30
    total_rows = len(df)
    total_pages = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)

    # Initialize session state for page tracking if not already done
    if "page" not in st.session_state:
        st.session_state.page = 0

    # Function to show the current page of data
    def show_page(page_number):
        start_row = page_number * rows_per_page
        end_row = start_row + rows_per_page
        return df[start_row:end_row]

    # Display the current page of the DataFrame as HTML (without the index column)
    page_data = show_page(st.session_state.page)
    table_html = page_data.to_html(index=False, escape=False)
    
    # Add custom CSS to increase font size
    custom_css = """
    <style>
        table {
            font-size: 20px;
        }
    </style>
    """
    # Inject the CSS into Streamlit app
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Display the table with the increased font size
    st.write(table_html, unsafe_allow_html=True)

    # Display navigation buttons and update the page state immediately after button press
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.page > 0:
            if st.button("Previous", key="prev"):
                st.session_state.page -= 1
                st.rerun()  # This will force a rerun to update the table immediately
    with col2:
        st.write(f"Page {st.session_state.page + 1} of {total_pages}")
    with col3:
        if st.session_state.page < total_pages - 1:
            if st.button("Next", key="next"):
                st.session_state.page += 1
                st.rerun()  # This will force a rerun to update the table immediately
else:
    st.error(output)

