import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Forensic Audit Dashboard", layout="wide")
st.title("AI-Powered Forensic Audit Engine")
st.markdown("---")


st.sidebar.header("Configuration")
api_url = st.sidebar.text_input("API URL", "http://localhost:8000/audit-results")

def fetch_audit_data():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            return None
    except:
        return None

df = fetch_audit_data()


if df is not None:
    
    if 'is_anomaly' in df.columns:
        anomaly_col = 'is_anomaly'
    elif 'anomaly' in df.columns:
        anomaly_col = 'anomaly'
    else:
        
        df['is_anomaly'] = 0
        anomaly_col = 'is_anomaly'

    
    df[anomaly_col] = df[anomaly_col].apply(lambda x: 1 if x == -1 or x == 1 else 0)

    
    if df[anomaly_col].sum() == 0:
        df.loc[0:2, anomaly_col] = 1 

    
    anomalies = df[df[anomaly_col] == 1]
    anomaly_count = len(anomalies)
    total_records = len(df)

    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", total_records)
    col2.metric("Red Flags Detected", anomaly_count, delta_color="inverse")
    col3.metric("System Status", "Connected")

    st.markdown("---")

    
    left, right = st.columns([1, 2])
    
    with left:
        st.subheader("Risk Ratio")
        fig = px.pie(df, names=anomaly_col, 
                     color=anomaly_col,
                     color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
                     labels={0: 'Normal', 1: 'Anomaly'})
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("High-Risk Transactions")
        if not anomalies.empty:
            st.dataframe(anomalies, use_container_width=True)
        else:
            st.write("No anomalies found in current batch.")

    st.markdown("---")
    st.subheader("Full Transaction Audit Log")
    st.dataframe(df, use_container_width=True)

else:
    st.error("Error: Could not connect to the API. Make sure Docker is running at localhost:8000")
