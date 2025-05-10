import streamlit as st
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re


def run_hadoop_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, check=True)
        output_lines = result.stdout.split("\n")
        filtered_lines = [line for line in output_lines if '|' in line]
        return "\n".join(filtered_lines)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


st.write("Day la trang cho mapreduce")

tasks = [
    "Select Task", 
    "10 do an co gia cao nhat", 
    "10 do an co gia thap nhat", 
    "10 quan an co danh gia cao nhat"
]

congviec = st.selectbox("Select Task", tasks, index=0)

if congviec != "Select Task":
    task = 0
    query = ""
    if congviec == "10 do an co gia cao nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/doan_top10_maxPrice && \
        hadoop jar /home/hadoopvuong/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopvuong/BigData_DoAn/project/task/MapperDoAnMaxPrice.py,/home/hadoopvuong/BigData_DoAn/project/task/ReducerDoAnMaxPrice.py \
        -mapper /home/hadoopvuong/BigData_DoAn/project/task/MapperDoAnMaxPrice.py \
        -reducer /home/hadoopvuong/BigData_DoAn/project/task/ReducerDoAnMaxPrice.py \
        -input /user/hadoopnhom3/BigData/DOAN \
        -output /user/hadoopnhom3/BigData/output/doan_top10_maxPrice && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/doan_top10_maxPrice/part-00000")
        task = 1

    elif congviec == "10 do an co gia thap nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/doan_top10_minPrice && \
        hadoop jar /home/hadoopvuong/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopvuong/BigData_DoAn/project/task/MapperDoAnMinPrice.py,/home/hadoopvuong/BigData_DoAn/project/task/ReducerDoAnMinPrice.py \
        -mapper /home/hadoopvuong/BigData_DoAn/project/task/MapperDoAnMinPrice.py \
        -reducer /home/hadoopvuong/BigData_DoAn/project/task/ReducerDoAnMinPrice.py \
        -input /user/hadoopnhom3/BigData/DOAN \
        -output /user/hadoopnhom3/BigData/output/doan_top10_minPrice && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/doan_top10_minPrice/part-00000")
        task = 2

    elif congviec == "10 quan an co danh gia cao nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/quanan_top10_maxRating && \
        hadoop jar /home/hadoopvuong/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopvuong/BigData_DoAn/project/task/MapperQuanAnMaxRating.py,/home/hadoopvuong/BigData_DoAn/project/task/ReducerQuanAnMaxRating.py \
        -mapper /home/hadoopvuong/BigData_DoAn/project/task/MapperQuanAnMaxRating.py \
        -reducer /home/hadoopvuong/BigData_DoAn/project/task/ReducerQuanAnMaxRating.py \
        -input /user/hadoopnhom3/BigData/QUANAN \
        -output /user/hadoopnhom3/BigData/output/quanan_top10_maxRating && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/quanan_top10_maxRating/part-00000")
        task = 3

    if query:
        output = run_hadoop_command(query)
        st.text(output)
        if  task == 1:
            data = [re.split(r"\s*\|\s*", line.strip()) for line in output.split('\n') if '|' in line]
            df = pd.DataFrame(data, columns=['Food', 'Price'])
            if not df.empty:
                try:
                    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                    df.dropna(inplace=True)

                    plt.figure(figsize=(10, 6))
                    sns.barplot(x='Price', y='Food', data=df, palette='viridis')
                    plt.title('Top 10 Most Expensive Foods')
                    plt.xlabel('Price')
                    plt.ylabel('Food')
                    plt.grid(axis='x', linestyle='--', alpha=0.7)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Error in plotting: {e}")
            else:
                st.warning("No data available to display.")
        if  task == 2:
            data = [re.split(r"\s*\|\s*", line.strip()) for line in output.split('\n') if '|' in line]
            df = pd.DataFrame(data, columns=['Food', 'Price'])
            if not df.empty:
                try:
                    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
                    df.dropna(inplace=True)

                    plt.figure(figsize=(10, 6))
                    sns.barplot(x='Price', y='Food', data=df, palette='viridis')
                    plt.title('Top 10 Cheapest Foods')
                    plt.xlabel('Price')
                    plt.ylabel('Food')
                    plt.grid(axis='x', linestyle='--', alpha=0.7)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Error in plotting: {e}")
            else:
                st.warning("No data available to display.")
        if  task == 3:
            data = [re.split(r"\s*\|\s*", line.strip()) for line in output.split('\n') if '|' in line]
            df = pd.DataFrame(data, columns=['Store', 'Rating'])
            if not df.empty:
                try:
                    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
                    df.dropna(inplace=True)

                    plt.figure(figsize=(10, 6))
                    sns.barplot(x='Rating', y='Store', data=df, palette='viridis')
                    plt.title('Top 10 Highest Rated Stores')
                    plt.xlabel('Rating')
                    plt.ylabel('Store')
                    plt.grid(axis='x', linestyle='--', alpha=0.7)
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Error in plotting: {e}")
            else:
                st.warning("No data available to display.")
