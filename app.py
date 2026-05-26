import streamlit as st
import pandas as pd
import io

# Page Configuration for Premium SaaS Look
st.set_page_config(page_title="Data Entry Titan Pro v3.0", page_icon="👑", layout="wide")

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
    .metric-box { padding: 15px; background-color: #F3F4F6; border-radius: 8px; border-left: 5px solid #2563EB; }
    </style>
""", unsafe_html=True)

st.markdown('<div class="main-title">👑 Data Entry Titan Pro v3.0</div>', unsafe_html=True)
st.markdown('<div class="sub-title">The All-In-One Data Wizard: Clean, Standardize, Filter, and Separate Anomalies in Seconds.</div>', unsafe_html=True)

# 1️⃣ FEATURE 1: Multi-Format Input Support
uploaded_file = st.file_uploader("📂 Upload your messy data file (Excel, CSV, or Text/Tab-Delimited)", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    try:
        # File type handling
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            # Handles tab-separated or comma-separated text files
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded and processed successfully!")
        
        # --- DATA PROCESSING ENGINE ---
        
        # 2️⃣ FEATURE 2: Smart Data Standardizer & Duplicate Remover
        # Remove exact duplicates
        df_processed = df.drop_duplicates()
        
        # Auto-capitalize names/cities/companies (Skip emails/URLs)
        for col in df_processed.select_dtypes(include=['object']).columns:
            col_lower = col.lower()
            if not any(x in col_lower for x in ['email', 'url', 'website', 'link']):
                df_processed[col] = df_processed[col].astype(str).str.strip().str.title()
            else:
                df_processed[col] = df_processed[col].astype(str).str.strip().str.lower()
        
        # 5️⃣ FEATURE 5: Bulletproof Anomaly & Trash Separator
        # Identify rows with any missing (NaN) values or empty strings
        is_anomaly = df_processed.isnull().any(axis=1) | (df_processed == "").any(axis=1) | (df_processed == "Nan").any(axis=1)
        
        df_anomalies = df_processed[is_anomaly]
        df_final_clean = df_processed[~is_anomaly]
        
        # 4️⃣ FEATURE 4: Automated AI-Style Summary & Metrics
        st.markdown("### 📊 Executive Insights & Metrics")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            st.markdown(f'<div class="metric-box"><b>Total Raw Rows:</b><br><span style="font-size:24px; color:#1E3A8A;">{len(df)}</span></div>', unsafe_html=True)
        with m_col2:
            duplicates_count = len(df) - len(df_processed)
            st.markdown(f'<div class="metric-box"><b>Duplicates Removed:</b><br><span style="font-size:24px; color:#DC2626;">{duplicates_count}</span></div>', unsafe_html=True)
        with m_col3:
            st.markdown(f'<div class="metric-box"><b>100% Clean Rows:</b><br><span style="font-size:24px; color:#16A34A;">{len(df_final_clean)}</span></div>', unsafe_html=True)
        with m_col4:
            anomaly_pct = (len(df_anomalies) / len(df_processed) * 100) if len(df_processed) > 0 else 0
            st.markdown(f'<div class="metric-box"><b>Anomaly Rate:</b><br><span style="font-size:24px; color:#EA580C;">{anomaly_pct:.1f}%</span></div>', unsafe_html=True)
            
        st.markdown("---")
        
        # 3️⃣ FEATURE 3: Interactive Search & Advanced Filter
        st.markdown("### 🔍 Interactive Live Dashboard")
        search_query = st.text_input("Type any keyword (Name, City, Company) to filter the clean dataset live:", "")
        
        display_clean_df = df_final_clean.copy()
        if search_query:
            # Filter rows that contain the search query in any column
            mask = display_clean_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
            display_clean_df = display_clean_df[mask]

        # Layout Tabs for organization
        tab1, tab2, tab3 = st.tabs(["✨ Clean Master File", "🚨 Anomaly & Trash Report", "📋 Original Raw Data"])
        
        with tab1:
            st.subheader("Pristine, Standardized & Filtered Records")
            st.dataframe(display_clean_df, use_container_width=True)
            
            # Download Clean File
            output_clean = io.BytesIO()
            with pd.ExcelWriter(output_clean, engine='openpyxl') as writer:
                df_final_clean.to_excel(writer, index=False, sheet_name='Clean_Master_Data')
            st.download_button(
                label="📥 Download Clean Master File (Excel)",
                data=output_clean.getvalue(),
                file_name="Clean_Master_File.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        with tab2:
            st.subheader("Defective or Missing Data Log")
            if len(df_anomalies) > 0:
                st.dataframe(df_anomalies, use_container_width=True)
                
                # Download Anomaly File
                output_anomaly = io.BytesIO()
                with pd.ExcelWriter(output_anomaly, engine='openpyxl') as writer:
                    df_anomalies.to_excel(writer, index=False, sheet_name='Anomalies_Log')
                st.download_button(
                    label="🚨 Download Anomaly & Trash Report (Excel)",
                    data=output_anomaly.getvalue(),
                    file_name="Anomaly_Trash_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.success("Flawless Dataset! No anomalies or missing values detected.")
                
        with tab3:
            st.subheader("Original File Uploaded By Client")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"System Error: Could not process file. Reason: {e}")
