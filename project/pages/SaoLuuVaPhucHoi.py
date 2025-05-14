import streamlit as st
import os
import subprocess

st.title("Sao lưu và phục hồi dữ liệu MySQL")

# Fixed Backup Directory
backup_dir = "/home/hadoopnhom3/BigData_DoAn/backup"

# Ensure the backup directory exists
os.makedirs(backup_dir, exist_ok=True)

# Backup Section
st.subheader("🔵 Sao lưu dữ liệu")
mysql_user = "root"  # Using root user
database_name = st.text_input("Nhập tên cơ sở dữ liệu để sao lưu:")

if st.button("Sao lưu"):
    if database_name:
        # Generate backup file path
        backup_file = os.path.join(backup_dir, f"{database_name}_backup.sql")

        # Backup command with sudo
        command = [
            "sudo", "mysqldump",
            "-u", mysql_user,
            database_name
        ]

        try:
            with open(backup_file, "wb") as f:
                process = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            if process.returncode == 0:
                st.success(f"Sao lưu thành công tại: {backup_file}")
            else:
                st.error(f"Đã xảy ra lỗi khi sao lưu: {process.stderr}")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi sao lưu: {str(e)}")
    else:
        st.warning("Vui lòng nhập tên cơ sở dữ liệu!")

# Restore Section
st.subheader("🟢 Phục hồi dữ liệu")
restore_user = "root"  # Using root user
uploaded_file = st.file_uploader("Chọn file SQL để phục hồi", type=["sql"])

if uploaded_file is not None:
    restore_database = st.text_input("Nhập tên cơ sở dữ liệu để phục hồi:")

    if st.button("Phục hồi"):
        if restore_database:
            # Save the uploaded file to the backup directory
            restore_path = os.path.join(backup_dir, uploaded_file.name)
            with open(restore_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Delete the existing database and create a new one
            delete_and_create_db_command = f"sudo mysql -u {mysql_user} -e 'DROP DATABASE IF EXISTS {restore_database}; CREATE DATABASE {restore_database};'"
            
            # Restore command
            restore_command = [
                "sudo", "mysql",
                "-u", restore_user,
                restore_database
            ]

            try:
                # Delete and create database
                process_delete_create = subprocess.run(delete_and_create_db_command, shell=True, stderr=subprocess.PIPE, text=True)
                if process_delete_create.returncode != 0:
                    st.error(f"Đã xảy ra lỗi khi xóa và tạo lại cơ sở dữ liệu: {process_delete_create.stderr}")

                # Restore the database
                with open(restore_path, "rb") as f:
                    process_restore = subprocess.run(restore_command, stdin=f, stderr=subprocess.PIPE, text=True)
                
                if process_restore.returncode == 0:
                    st.success(f"Phục hồi thành công từ: {uploaded_file.name}")
                else:
                    st.error(f"Đã xảy ra lỗi khi phục hồi: {process_restore.stderr}")
            except Exception as e:
                st.error(f"Đã xảy ra lỗi khi phục hồi: {str(e)}")
        else:
            st.warning("Vui lòng nhập tên cơ sở dữ liệu để phục hồi!")

