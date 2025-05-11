import streamlit as st
import subprocess

def run_sqoop_eval(query):
    command = [
        "sqoop", "eval",
        "--connect", "jdbc:mysql://localhost/QuanLyQuanAn",
        "--username", "sqoopdb",
        "--password", "Abc123456!@#",
        "--query", query
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout

    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

st.title("Insert into DOAN")

input_id = st.text_input("Insert your Restaurant ID here...")
input_tenDoAn = st.text_input("Insert your Food Name here...")
input_price = st.number_input("Insert your Price here...", min_value=0.0, format="%.2f")

btn_create = st.button("Insert")

if btn_create:
    # Check if ID is numeric and not empty
    if input_id.isdigit():
        # Check if the Restaurant ID exists
        check_query = f"SELECT rating FROM QUANAN WHERE id = {input_id}"
        rating_output = run_sqoop_eval(check_query)

        # Try to parse the rating from the output
        try:
            rating = None
            lines = rating_output.split("\n")
            
            # Skip header and find the actual rating value in the output
            for line in lines:
                line = line.strip()
                if "|" in line:  # Focus on lines with data, separated by "|"
                    parts = line.split("|")
                    if len(parts) == 3:  # Expected 3 parts: left separator, rating label, right separator
                        rating = parts[1].strip()  # Extract and clean the middle part
                        if rating.lower() != 'rating':  # Ensure it's not the header
                            break

            if rating is None:
                raise ValueError(f"Restaurant ID {input_id} not found in QUANAN table.")

        except ValueError as e:
            st.error(f"Error: {e}. Restaurant ID {input_id} not found or invalid data.")
            st.stop()

        # Construct the insert query
        query = f"""
        INSERT INTO DOAN (idquan, item, price, rating)
        VALUES ({input_id}, '{input_tenDoAn}', {input_price}, '{rating}')
        """
        
        # Execute the insert query
        output = run_sqoop_eval(query)

        if "Error" not in output:
            st.success("Insert successfully!")
        else:
            st.error(f"Insert failed: {output}")
    
    else:
        st.error("Please enter a valid numeric Restaurant ID.")

