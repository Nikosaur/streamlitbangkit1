# Import Library yang diperlukan
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Weather Dashboard",
                   page_icon="🌤",
                   layout="wide")

# Menyembunyikan UI streamlit
hide_st = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st, unsafe_allow_html=True)

# Header
st.header("🌤Weather Report Dashboard")
st.write("Showing the weather in 2013 near Changping station")

# Memasukkan data
df = pd.read_csv("PRSA_Data_Changping_20130301-20170228.csv")

# Mengganti nama kolom data supaya lebih mudah digunakan
df.rename(columns={'PM2.5': 'PM25'}, inplace=True)

# Imputasi data
df['PM25'].fillna(value=df['PM25'].mean(), inplace=True)
df['PM10'].fillna(value=df['PM10'].mean(), inplace=True)
df['SO2'].fillna(value=df['SO2'].mean(), inplace=True)
df['NO2'].fillna(value=df['NO2'].mean(), inplace=True)
df['CO'].fillna(value=df['CO'].mean(), inplace=True)
df['O3'].fillna(value=df['O3'].mean(), inplace=True)
df['TEMP'].fillna(value=df['TEMP'].mean(), inplace=True)
df['PRES'].fillna(value=df['PRES'].mean(), inplace=True)
df['DEWP'].fillna(value=df['DEWP'].mean(), inplace=True)
df['RAIN'].fillna(value=df['RAIN'].mean(), inplace=True)
mode_wd = df['wd'].mode()[0]
df['wd'].fillna(mode_wd, inplace=True)
df['WSPM'].fillna(value=df['WSPM'].mean(), inplace=True)

# Membuat kolom baru untuk Bulan
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

df.set_index('date', inplace=True)

# Checkbox untuk menampilkan dan menghilangkan DataFrame
show_df = st.checkbox('Show DataFrame')

if show_df:
    st.write(df)

# Sidebar
# Faktor yang mempengaruhi hujan
st.sidebar.header("Rain Factors:")

# Multiselect untuk menampilkan pengaruh faktor terhadap hujan
affect_rain = st.sidebar.multiselect(
    'Which factors do you want to display?',
    ('TEMP', 'PRES', 'DEWP', 'WSPM')
)

# Plot sesuai dengan seleksi menggunakan scatter
for factors in affect_rain:
    fig = px.scatter(df, x=factors, y='RAIN', title=f'{factors} vs Rainfall')
    fig.update_layout(xaxis_title=factors, yaxis_title='Rainfall (mm)')
    st.plotly_chart(fig)

st.sidebar.header("Air Condition per Month:")

# Multiselect untuk menampilkan kondisi udara per bulan
conditions = st.sidebar.multiselect(
    'Which air condition do you want to display?',
    ('TEMP', 'PRES', 'DEWP', 'WSPM')
)

# Plot sesuai dengan seleksi menggunakan line chart
for condition in conditions:
    filtered_df = df[condition]
    fig = px.line(filtered_df, x=filtered_df.index.month, y=filtered_df, title=f'Average {condition} Change per Month')
    fig.update_layout(xaxis=dict(range=[1, 12]), yaxis_title=f'Average {condition}', xaxis_title='Month')
    st.plotly_chart(fig)

# Checkbox untuk menampilkan dan menghilangkan hujan per bulan
rain_opt = st.sidebar.checkbox('Show Rainfall')

if rain_opt:
    # Mengumpulkan data hujan untuk menghitung hujan per bulan
    monthly_rain = df.resample('M').sum()

    # Visualisasi hujan per bulan
    fig = px.line(monthly_rain, x=monthly_rain.index.month, y='RAIN', title='Monthly Rainfall')
    fig.update_layout(xaxis=dict(range=[1, 12]), yaxis_title='Total Rainfall (mm)', xaxis_title='Month')
    st.plotly_chart(fig)

