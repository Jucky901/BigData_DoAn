import streamlit as st
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter



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
    "10 quan an co danh gia cao nhat",
    "Gia trung binh cac mon ăn trong quan",
    "Thong ke so quan ban theo so mon an"
]

congviec = st.selectbox("Select Task", tasks, index=0)

if congviec != "Select Task":
    task = 0
    query = ""
    if congviec == "10 do an co gia cao nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/doan_top10_maxPrice || \
        hadoop jar /home/hadoopnhom3/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopnhom3/BigData_DoAn/project/task/MapperDoAnMaxPrice.py,/home/hadoopnhom3/BigData_DoAn/project/task/ReducerDoAnMaxPrice.py \
        -mapper /home/hadoopnhom3/BigData_DoAn/project/task/MapperDoAnMaxPrice.py \
        -reducer /home/hadoopnhom3/BigData_DoAn/project/task/ReducerDoAnMaxPrice.py \
        -input /user/hadoopnhom3/BigData/DOAN/part-00000 \
        -output /user/hadoopnhom3/BigData/output/doan_top10_maxPrice && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/doan_top10_maxPrice/part-00000")
        task = 1

    elif congviec == "10 do an co gia thap nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/doan_top10_minPrice || \
        hadoop jar /home/hadoopnhom3/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopnhom3/BigData_DoAn/project/task/MapperDoAnMinPrice.py,/home/hadoopnhom3/BigData_DoAn/project/task/ReducerDoAnMinPrice.py \
        -mapper /home/hadoopnhom3/BigData_DoAn/project/task/MapperDoAnMinPrice.py \
        -reducer /home/hadoopnhom3/BigData_DoAn/project/task/ReducerDoAnMinPrice.py \
        -input /user/hadoopnhom3/BigData/DOAN \
        -output /user/hadoopnhom3/BigData/output/doan_top10_minPrice && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/doan_top10_minPrice/part-00000")
        task = 2

    elif congviec == "10 quan an co danh gia cao nhat":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/quanan_top10_maxRating || \
        hadoop jar /home/hadoopnhom3/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopnhom3/BigData_DoAn/project/task/MapperQuanAnMaxRating.py,/home/hadoopnhom3/BigData_DoAn/project/task/ReducerQuanAnMaxRating.py \
        -mapper /home/hadoopnhom3/BigData_DoAn/project/task/MapperQuanAnMaxRating.py \
        -reducer /home/hadoopnhom3/BigData_DoAn/project/task/ReducerQuanAnMaxRating.py \
        -input /user/hadoopnhom3/BigData/QUANAN \
        -output /user/hadoopnhom3/BigData/output/quanan_top10_maxRating && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/quanan_top10_maxRating/part-00000")
        task = 3

    elif congviec == "Gia trung binh cac mon ăn trong quan":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/avg_price_per_quan && \
        hadoop jar /home/hadoopnhom3/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -files /home/hadoopnhom3/BigData_DoAn/project/task/Mapper_AvgPrice.py,/home/hadoopnhom3/BigData_DoAn/project/task/Reducer_AvgPrice.py \
        -mapper /home/hadoopnhom3/BigData_DoAn/project/task/Mapper_AvgPrice.py \
        -reducer /home/hadoopnhom3/BigData_DoAn/project/task/Reducer_AvgPrice.py \
        -input /user/hadoopnhom3/BigData/QUANAN \
        -output /user/hadoopnhom3/BigData/output/avg_price_per_quan && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/avg_price_per_quan/part-00000")
        task = 4
    
    elif congviec == "Thong ke so quan ban theo so mon an":
        query = ("hdfs dfs -rm -r /user/hadoopnhom3/BigData/output/count_items_per_quan && \
        hadoop jar /home/hadoopnhom3/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar \
        -file /home/hadoopnhom3/Mapreduce/MapperDemMonAn.py -mapper /home/hadoopnhom3/Mapreduce/MapperDemMonAn.py \
        -file /home/hadoopnhom3/Mapreduce/ReducerDemMonAn.py -reducer /home/hadoopnhom3/Mapreduce/ReducerDemMonAn.py \
        -input /user/hadoopnhom3/BigData/DOAN \
        -output /user/hadoopnhom3/BigData/output/count_items_per_quan && \
        hdfs dfs -cat /user/hadoopnhom3/BigData/output/count_items_per_quan/part-00000")
        task = 5


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
        if  task == 4:
            data = [re.split(r"\s*\|\s*", line.strip()) for line in output.split('\n') if '|' in line]
            df = pd.DataFrame(data, columns=['Idquan', 'AVG'])
            if not df.empty:
                try:

                    df['AVG'] = pd.to_numeric(df['AVG'], errors='coerce')
                    df.dropna(inplace=True)
                    bins = [0, 20000, 40000, 60000, 80000, 100000, np.inf]
                    labels = ['< 20k', '20k - 40k', '40k - 60k', '60k - 80k', '80k - 100k', '> 100k']
                    df['khoang_gia'] = pd.cut(df['avg_gia_mon_an'], bins=bins, labels=labels, right=False)
                    phan_tram_quan = df['khoang_gia'].value_counts(normalize=True) * 100
                    phan_tram_quan = phan_tram_quan.sort_index()
                    plt.figure(figsize=(10, 6))
                    plt.hist(df['AVG'], bins=bins, weights=np.ones(len(df)) / len(df) * 100, edgecolor='black', alpha=0.7)
                    plt.xlabel('Giá trung bình món ăn')
                    plt.ylabel('Phần trăm số quán')
                    plt.title('Phân phối phần trăm quán theo giá trung bình món ăn')
                    plt.xticks(bins)
                    plt.grid(axis='y', linestyle='--')
                    plt.tight_layout()
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Error in plotting: {e}")
            else:
                st.warning("No data available to display.")
        if task == 5:
            # Giả sử output là dữ liệu đầu vào của bạn (dưới dạng string hoặc file)
            data = [re.split(r"\s*\|\s*", line.strip()) for line in output.split('\n') if '|' in line]
            df = pd.DataFrame(data, columns=['Idquan', 'SL'])

            # Chuyển đổi số lượng món ăn (SL) thành kiểu số nguyên
            df['SL'] = pd.to_numeric(df['SL'], errors='coerce')
            df = df.dropna(subset=['SL'])
            # Đếm số lượng quán theo số món ăn
            count_dict = Counter(df['SL'])

            # Chuyển dữ liệu đếm thành DataFrame
            df_count = pd.DataFrame(count_dict.items(), columns=['Số_món_ăn', 'Số_lượng_quán'])
            df_count = df_count.sort_values(by='Số_món_ăn')

            if not df_count.empty:
                try:
                    # Vẽ biểu đồ
                    plt.figure(figsize=(10, 6))
                    plt.bar(df_count['Số_món_ăn'], df_count['Số_lượng_quán'], color='skyblue')
                    plt.xlabel('Số món ăn/quán')
                    plt.ylabel('Số lượng quán')
                    plt.title('Biểu đồ: Số lượng quán theo số món ăn')
                    plt.xticks(df_count['Số_món_ăn'])
                    plt.grid(axis='y', linestyle='--', alpha=0.7)
                    plt.tight_layout()
                    st.pyplot(plt)
                except Exception as e:
                    st.error(f"Error in plotting: {e}")
            else:
                st.warning("No data available to display.")


