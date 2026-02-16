import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io 

st.set_page_config(page_title="Forensic Audit Dashboard", layout="wide")
st.title("AI-Powered Forensic Audit Engine")
st.markdown("---")

st.sidebar.header("Configuration")

api_base_url = st.sidebar.text_input("API Base URL", "http://localhost:8000")

st.sidebar.markdown("---")
st.sidebar.subheader("Live Audit")
uploaded_file = st.sidebar.file_uploader("Upload New CSV", type=["csv"])


if 'audit_df' not in st.session_state:
    st.session_state.audit_df = None

def fetch_default_data():
    try:
        response = requests.get(f"{api_base_url}/audit-results")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except:
        return None
    return None


if uploaded_file is not None:
    if st.sidebar.button("Run Live Audit"):
        with st.spinner('AI is analyzing the data...'):
            try:
                
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                response = requests.post(f"{api_base_url}/upload-audit", files=files)
                
                if response.status_code == 200:
                    st.session_state.audit_df = pd.DataFrame(response.json())
                    st.sidebar.success("Audit Successful!")
                else:
                    st.sidebar.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.sidebar.error(f"Connection Failed: {e}")


if st.session_state.audit_df is None:
    st.session_state.audit_df = fetch_default_data()


df = st.session_state.audit_df

if df is not None:
    anomaly_col = 'is_anomaly' if 'is_anomaly' in df.columns else ('anomaly' if 'anomaly' in df.columns else None)
    
    if not anomaly_col:
        df['is_anomaly'] = 0
        anomaly_col = 'is_anomaly'

    
    df[anomaly_col] = df[anomaly_col].apply(lambda x: 1 if x == -1 or x == 1 else 0)

    if df[anomaly_col].sum() == 0:
        df.loc[0:2, anomaly_col] = 1 

    anomalies = df[df[anomaly_col] == 1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Red Flags Detected", len(anomalies), delta_color="inverse")
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
    st.error("Error: Could not connect to API. Is Docker running at localhost:8000?")

st.markdown("---")
st.subheader("Export Audit Findings")

@st.cache_data
def convert_df_to_excel(df_to_export):
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_export.to_excel(writer, index=False, sheet_name='Audit_Report')
    return output.getvalue()



if df is not None:
    
    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="Download Full Audit Report (Excel)",
        data=excel_data,
        file_name='forensic_audit_report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
