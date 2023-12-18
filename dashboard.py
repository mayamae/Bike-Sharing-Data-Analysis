# Library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Function
def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.sum().reset_index()
    byhour_df.rename(columns={
        "hr": "jam",
        "cnt": "total_peminjaman"
    }, inplace=True)
    return byhour_df

def create_byseason_df(df):
    byseason_df = df.groupby(by=["season","temp"]).cnt.sum().reset_index()
    byseason_df.rename(columns={
        "season": "Season",
        "temp": "suhu",
        "cnt": "total_peminjaman"
    }, inplace=True)
    return byseason_df

#Load csv
main_df = pd.read_csv("main_data.csv")

main_df["dteday"] = pd.to_datetime(main_df["dteday"])
# Membuat komponen filter
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_date_df = main_df[(main_df["dteday"] >= str(start_date)) & 
                (main_df["dteday"] <= str(end_date))]

byhour_df = create_byhour_df(main_date_df)
byseason_df = create_byseason_df(main_date_df)

st.header('Bike Sharing Dashboard')

col1, col2= st.columns(2)
 
with col1:
    total_rental = byhour_df["total_peminjaman"].sum()
    st.metric("Total rental", value=total_rental)

st.subheader('Number of Bike Rentals per Hour')
fig, ax = plt.subplots(figsize=(30, 15))
 
sns.barplot(
    y="total_peminjaman",
    x="jam",
    data=byhour_df,
    ax=ax
)
#ax.set_title("Number of Bike Rentals per Hour", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader('Number of Bike Rentals by Season and Temperature')
fig, ax = plt.subplots(figsize=(30, 15))
 
sns.set(font_scale=2.5)
sns.scatterplot(
    data=byseason_df,
    x="suhu",
    y="total_peminjaman",
    hue="Season",
    style="Season"
)
#ax.set_title("Number of Bike Rentals by Season and Temperature", loc="center", fontsize=50)
ax.set_ylabel("Total Rental", fontsize=30)
ax.set_xlabel("Temperature (degC)", fontsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)