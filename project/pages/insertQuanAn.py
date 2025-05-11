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

st.title("Thêm dữ liệu vào bảng quán ăn")

input_tenQuanAn = st.text_input("Insert your Restaurant name here...")
input_diachi = st.text_input("Insert your Address here...")
input_rating = st.selectbox("Select Rating", [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], index=0)

btn_create = st.button("Insert")

if btn_create:
    # First, get the max ID
    max_id_query = "SELECT MAX(id) AS max_id FROM QUANAN"
    max_id_output = run_sqoop_eval(max_id_query)

    # Initialize max_id to 1 in case the table is empty or the query fails
    max_id = 1

    # Process the output
    for line in max_id_output.split("\n"):
        line = line.strip()
        # Ignore warning lines and headers
        if "Warning" in line or "|" not in line:
            continue

        # Extract the value inside the pipe symbols
        parts = line.split("|")
        if len(parts) >= 2:
            try:
                # Attempt to convert the second part to an integer
                potential_id = parts[1].strip()
                max_id = int(potential_id) + 1
                break  # Exit once we have the value
            except ValueError:
                continue

    # Construct the insert query
    query = f"""
    INSERT INTO QUANAN (id, tenquan, diachi, rating)
    VALUES ({max_id}, '{input_tenQuanAn}', '{input_diachi}', {input_rating})
    """

    # Run the insert query
    output = run_sqoop_eval(query)

    if "Error" not in output:
        st.success(f"Insert successfully! New ID: {max_id}")
    else:
        st.error(f"Insert failed: {output}")

