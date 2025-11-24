"""
Annual Temperature Anomalies Analysis
Developer: Matthew Pool
Data Source: NASA GISS Surface Temperature Analysis
https://data.giss.nasa.gov/gistemp/
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Global Temperature Anomalies",
    page_icon="🌡️",
    layout="wide"
)

# Title and description
st.title("🌡️ Annual Global Surface Temperature Anomalies")
st.markdown("""
Analysis of annual temperature deviation from the long-term average temperature,
based on NASA's global surface temperature dataset.
""")

# Load data
@st.cache_data
def load_data():
    """Load and preprocess temperature data"""
    try:
        df = pd.read_csv('temperatures.csv', skiprows=1)
        
        monthly_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Clean data
        df[monthly_columns] = df[monthly_columns].replace({'***': np.nan}).astype(float)
        
        # Calculate annual mean
        df['Annual_Mean'] = df[monthly_columns].mean(axis=1)
        
        return df, monthly_columns
    except FileNotFoundError:
        st.error("⚠️ Data file 'temperatures.csv' not found. Please ensure it's in the same directory.")
        return None, None

df, monthly_columns = load_data()

if df is not None:
    # Sidebar controls
    st.sidebar.header("Visualization Options")
    
    chart_type = st.sidebar.selectbox(
        "Chart Type",
        ["Line Chart", "Scatter Plot", "Both"]
    )
    
    show_trend = st.sidebar.checkbox("Show Polynomial Trend Line", value=True)
    
    if show_trend:
        degree = st.sidebar.slider("Polynomial Degree", 1, 5, 3)
    
    show_baseline = st.sidebar.checkbox("Show Average Temperature Baseline", value=True)
    
    year_range = st.sidebar.slider(
        "Year Range",
        int(df['Year'].min()),
        int(df['Year'].max()),
        (int(df['Year'].min()), int(df['Year'].max()))
    )
    
    # Filter data by year range
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    
    # Create visualization
    st.subheader("Temperature Anomaly Visualization")
    
    # Using Plotly for interactivity
    fig = go.Figure()
    
    # Add line chart
    if chart_type in ["Line Chart", "Both"]:
        fig.add_trace(go.Scatter(
            x=filtered_df['Year'],
            y=filtered_df['Annual_Mean'],
            mode='lines',
            name='Annual Mean',
            line=dict(color='blue', width=2)
        ))
    
    # Add scatter plot
    if chart_type in ["Scatter Plot", "Both"]:
        fig.add_trace(go.Scatter(
            x=filtered_df['Year'],
            y=filtered_df['Annual_Mean'],
            mode='markers',
            name='Data Points',
            marker=dict(color='blue', size=4)
        ))
    
    # Add polynomial trend line
    if show_trend:
        x = filtered_df['Year']
        y = filtered_df['Annual_Mean']
        coef = np.polyfit(x, y, degree)
        polynomial = np.poly1d(coef)
        y_poly_fit = polynomial(x)
        
        fig.add_trace(go.Scatter(
            x=x,
            y=y_poly_fit,
            mode='lines',
            name=f'Trend (Degree {degree})',
            line=dict(color='red', width=2, dash='solid')
        ))
    
    # Add baseline
    if show_baseline:
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="gray",
            annotation_text="Average Temperature",
            annotation_position="right"
        )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Temperature Deviation (°C)",
        hovermode='x unified',
        template='plotly_white',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.subheader("Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Anomaly", f"{filtered_df['Annual_Mean'].mean():.2f}°C")
    
    with col2:
        st.metric("Maximum Anomaly", f"{filtered_df['Annual_Mean'].max():.2f}°C")
    
    with col3:
        st.metric("Minimum Anomaly", f"{filtered_df['Annual_Mean'].min():.2f}°C")
    
    with col4:
        st.metric("Std Deviation", f"{filtered_df['Annual_Mean'].std():.2f}°C")
    
    # Show data table
    if st.checkbox("Show Raw Data"):
        st.dataframe(filtered_df[['Year'] + monthly_columns + ['Annual_Mean']], use_container_width=True)
    
    # Download section
    st.subheader("Export Data")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"temperature_anomalies_{year_range[0]}-{year_range[1]}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Developer:** Matthew Pool  
    **Data Source:** [NASA GISS Surface Temperature Analysis](https://data.giss.nasa.gov/gistemp/)  
    **Purpose:** Analysis of annual temperature deviations from long-term averages
    """)