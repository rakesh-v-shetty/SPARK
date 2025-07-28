import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# Configure page
st.set_page_config(
    page_title="SPARK - Sustainable Power Analysis & Renewable Kinetics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        color: #e0e0e0;
        margin-bottom: 2rem;
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #cccccc;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 1px solid #444;
        padding-bottom: 0.25rem;
    }

    .metric-card {
        background-color: #1e1e1e;
        padding: 1.25rem;
        border-radius: 8px;
        border-left: 4px solid #555;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .info-box {
        background-color: #262626;
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid #3a3a3a;
        margin: 1rem 0;
    }

    .info-box h2, .info-box h3 {
        color: #e0e0e0;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .info-box h2:first-child {
        margin-top: 0;
    }

    .info-box p {
        color: #cccccc;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .info-box ul {
        color: #cccccc;
        line-height: 1.6;
        margin-bottom: 1rem;
        padding-left: 1.5rem;
    }

    .info-box li {
        margin-bottom: 0.5rem;
    }

    .info-box strong {
        color: #00b894;
        font-weight: 600;
    }

    .stSelectbox > div > div {
        background-color: #1e1e1e !important;
        border: 1px solid #3a3a3a !important;
        color: #e0e0e0 !important;
    }

    .stDateInput > div > div {
        background-color: #1e1e1e !important;
        border: 1px solid #3a3a3a !important;
        color: #e0e0e0 !important;
    }

    .stCheckbox > div > div {
        background-color: #1e1e1e !important;
        border: 1px solid #3a3a3a !important;
        color: #e0e0e0 !important;
    }

    .stCheckbox > div > div > label {
        color: #e0e0e0 !important;
        font-size: 0.9rem !important;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }

    .metric-card-compact {
        background-color: #1e1e1e;
        padding: 0.75rem;
        border-radius: 6px;
        border-left: 3px solid #555;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Load renewable and non-renewable energy data
@st.cache_data
def load_energy_data():
    """Load energy data from CSV files"""
    try:
        # Load daily renewable data
        daily_renewable = pd.read_csv('./mapreduce/renewable/dailyenergy/daily.csv')
        daily_renewable['Date'] = pd.to_datetime(daily_renewable['time'], format='%d-%m-%y')
        
        # Load weekly renewable data
        weekly_renewable = pd.read_csv('./mapreduce/renewable/weeklyenergy/weekly.csv')
        
        # Load monthly renewable data
        monthly_renewable = pd.read_csv('./mapreduce/renewable/monthlyenergy/monthly.csv')
        
        # Load daily non-renewable data
        daily_nonrenewable = pd.read_csv('./mapreduce/nonrenewable/dailyenergy/daily.csv')
        daily_nonrenewable['Date'] = pd.to_datetime(daily_nonrenewable['time'], format='%d-%m-%y')
        
        # Load weekly non-renewable data
        weekly_nonrenewable = pd.read_csv('./mapreduce/nonrenewable/weeklyenergy/weekly.csv')
        
        # Load monthly non-renewable data
        monthly_nonrenewable = pd.read_csv('./mapreduce/nonrenewable/monthlyenergy/monthly.csv')
        
        # Load fossil fuel dependency data
        fossil_fuel_dependency = pd.read_csv('./mapreduce/FossilFuelDependency/ffd.csv')
        # Strip whitespace from column names to handle any leading/trailing spaces
        fossil_fuel_dependency.columns = fossil_fuel_dependency.columns.str.strip()
        
        return {
            'daily_renewable': daily_renewable,
            'weekly_renewable': weekly_renewable,
            'monthly_renewable': monthly_renewable,
            'daily_nonrenewable': daily_nonrenewable,
            'weekly_nonrenewable': weekly_nonrenewable,
            'monthly_nonrenewable': monthly_nonrenewable,
            'fossil_fuel_dependency': fossil_fuel_dependency
        }
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        return None

# # Generate sample data for ML analysis
# @st.cache_data
# def generate_sample_ml_data():
#     # Generate sample load forecast data
#     dates = pd.date_range(start='2015-01-01', end='2018-12-31', freq='D')
#     load_data = pd.DataFrame({
#         'Date': dates,
#         'Actual_Load': np.random.normal(1000, 200, len(dates)) + 100 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
#         'Predicted_Load': np.random.normal(1000, 180, len(dates)) + 100 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365),
#         'Temperature': np.random.normal(20, 10, len(dates)),
#         'Humidity': np.random.uniform(30, 90, len(dates))
#     })
#     return load_data

# Load data
energy_data = load_energy_data()
ml_load_data = pd.read_csv('./data/forecast.csv')

# Define renewable energy columns
RENEWABLE_COLUMNS = [
    'generation biomass',
    'generation geothermal',
    'generation hydro pumped storage consumption',
    'generation hydro run-of-river and poundage',
    'generation hydro water reservoir',
    'generation marine',
    'generation nuclear',
    'generation other renewable',
    'generation solar',
    'generation waste',
    'generation wind offshore',
    ' generation wind onshore'  # Note the leading space
]

# Define non-renewable energy columns
NONRENEWABLE_COLUMNS = [
    'generation fossil brown coal/lignite',
    'generation fossil coal-derived gas',
    'generation fossil gas',
    'generation fossil hard coal',
    'generation fossil oil',
    'generation fossil oil shale',
    'generation fossil peat'
]

# Define fossil fuel dependency columns
FOSSIL_FUEL_DEPENDENCY_COLUMNS = [
    'avgLoad',
    'avgTotalFossil',  # Now without leading space after stripping
    'avgTotalGeneration',
    'fossilDependencyPercent',
    'avgBrownCoal',
    'avgCoalGas',
    'avgNaturalGas',
    'avgHardCoal',
    'avgOil',
    'avgOilShale',
    'avgPeat',
    'brownCoalPercent',
    'coalGasPercent',
    'naturalGasPercent',
    'hardCoalPercent',
    'oilPercent',
    'count'
]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["Home", "📊 Data Analysis","👾 ML Analysis"]
)

if page == "Home":
    st.markdown('<h1 class="main-header">⚡ SPARK – Sustainable Power Analytics and Renewable Kinetics</h1>', unsafe_allow_html=True)
    
    # Project Overview Section
    st.markdown("""
    <div class="info-box">
        <h2>Project Overview</h2>
        <p>
            This platform provides comprehensive tools for energy forecasting and deep analytics of both renewable and non-renewable energy sources, leveraging machine learning for sustainable power insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features Section
    st.markdown('<h3 style="color: #e0e0e0; margin-top: 1.5rem; margin-bottom: 0.5rem;">Key Features</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - **Load Forecasting:** Accurate energy demand prediction using ML algorithms
        - **Renewable Energy Analysis:** Insights into solar, wind, and other renewable sources
        - **Non-Renewable Analysis:** Evaluation of coal, gas, oil, and nuclear energy generation
        """)
    
    with col2:
        st.markdown("""
        - **Correlation Analysis:** Examine interdependencies between key energy metrics
        - **Seasonal Trends:** Discover fossil fuel usage patterns across different seasons
        """)
    
    # Objectives Section
    st.markdown('<h3 style="color: #e0e0e0; margin-top: 1.5rem; margin-bottom: 0.5rem;">Objectives</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - Enhance grid efficiency through predictive analytics
        - Encourage renewable adoption with actionable insights
        """)
    
    with col2:
        st.markdown("""
        - Reduce fossil dependency via informed planning
        - Support energy policy with evidence-based analysis
        """)

    # Stats Overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Historical Data</h4>
            <h2>35K+</h2>
            <p>Hours analyzed</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Forecast Accuracy</h4>
            <h2>95.2%</h2>
            <p>Avg. model performance</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Renewable Share</h4>
            <h2>34.7%</h2>
            <p>Current clean energy usage</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>Peak Load in an hour</h4>
            <h2>41,015 MW</h2>
            <p>Max recorded demand</p>
        </div>
        """, unsafe_allow_html=True)

# DATA ANALYSIS PAGE
elif page == "📊 Data Analysis":
    st.markdown('<h1 class="main-header">📊 Data Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h2>🔍 Data Analysis Overview</h2>
        <p>Comprehensive analysis of energy generation patterns, renewable vs non-renewable sources, and seasonal dependencies:</p>
        <ul>
            <li><strong>Renewable Energy:</strong> Solar, wind, and other clean energy sources analysis</li>
            <li><strong>Non-Renewable Energy:</strong> Coal, natural gas, nuclear, and oil generation patterns</li>
            <li><strong>Seasonal Analysis:</strong> Fossil fuel dependency across different seasons</li>
            <li><strong>Comparative Studies:</strong> Interactive comparison between different energy sources</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data is loaded
    if energy_data is None:
        st.error("❌ Unable to load energy data. Please check if the CSV files are available in the correct directory structure.")
        st.stop()
    
    # Analysis type selection
    st.markdown('<h2 class="section-header">⚙️ Analysis Configuration</h2>', unsafe_allow_html=True)
    
    analysis_type = st.selectbox(
        "Choose Analysis Type:",
        ["Renewables", "Non-Renewables", "Fossil Fuel Dependency"]
    )
    
    # Time range selection with validation (only for Renewables and Non-Renewables)
    if analysis_type in ["Renewables", "Non-Renewables"]:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2015, 1, 1), key="data_start")
        with col2:
            end_date = st.date_input("End Date", datetime(2018, 12, 31), key="data_end")
        
        # Validate date range
        min_date = datetime(2015, 1, 1).date()
        max_date = datetime(2018, 12, 31).date()
        
        if start_date < min_date or end_date > max_date or start_date > max_date or end_date < min_date:
            st.markdown("""
            <div style="background-color: #ff4444; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>⚠️ Invalid Date Range</strong><br>
                Please choose dates between <strong>01/01/2015</strong> and <strong>31/12/2018</strong>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        
        # Validate that start_date is before end_date
        if start_date >= end_date:
            st.markdown("""
            <div style="background-color: #ff4444; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>⚠️ Invalid Date Range</strong><br>
                Start date must be <strong>before</strong> end date
            </div>
            """, unsafe_allow_html=True)
            st.stop()
    
    if analysis_type == "Renewables":
        st.markdown('<h2 class="section-header">🌱 Renewable Energy Analysis</h2>', unsafe_allow_html=True)
        
        # Chart type selection
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox("Chart Type:", ["Line Chart", "Stacked Area Chart", "Pie Chart"])
        with col2:
            time_resolution = st.selectbox("Time Resolution:", ["Daily", "Weekly", "Monthly"])
        
        # Get the appropriate dataset and convert time to Date
        if time_resolution == "Daily":
            renewable_df = energy_data['daily_renewable']
            # Date column already created in load_energy_data()
        elif time_resolution == "Weekly":
            renewable_df = energy_data['weekly_renewable']
            # Convert weekly time format (e.g., "2015-W01") to datetime
            # Use a simpler approach: extract year and week, then create datetime
            def parse_iso_week(week_str):
                year, week = week_str.split('-W')
                # Create a datetime for the first day of the year, then add weeks
                first_day = pd.Timestamp(year=int(year), month=1, day=1)
                # Find the first Monday of the year
                while first_day.weekday() != 0:  # Monday is 0
                    first_day += pd.Timedelta(days=1)
                # Add the weeks
                return first_day + pd.Timedelta(weeks=int(week)-1)
            
            renewable_df['Date'] = renewable_df['time'].apply(parse_iso_week)
        else:  # Monthly
            renewable_df = energy_data['monthly_renewable']
            # Convert monthly time format (e.g., "2015-01") to datetime
            renewable_df['Date'] = pd.to_datetime(renewable_df['time'] + '-01', format='%Y-%m-%d')
        
        # Column selection
        st.markdown('<h3 class="section-header">📋 Select Energy Sources</h3>', unsafe_allow_html=True)
        
        # Filter columns that exist in the dataset
        available_columns = [col for col in RENEWABLE_COLUMNS if col in renewable_df.columns]
        
        if not available_columns:
            st.error("❌ No renewable energy columns found in the dataset.")
            st.stop()
        
        # Initialize session state for selections
        if 'renewable_selections' not in st.session_state:
            st.session_state.renewable_selections = []
        
        # Add Select All and Clear All buttons
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to move buttons down
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Select All", key="select_all_renewable"):
                st.session_state.renewable_selections = available_columns.copy()
                st.rerun()
        with col2:
            if st.button("Clear All", key="clear_all_renewable"):
                st.session_state.renewable_selections = []
                st.rerun()
        with col3:
            pass  # Empty column for symmetry
        with col4:
            pass  # Empty column for symmetry
        
        # Use a more organized grid layout for checkboxes
        if len(available_columns) <= 6:
            # For 6 or fewer columns, use 3 columns
            col1, col2, col3 = st.columns(3)
            
            for i, column in enumerate(available_columns):
                with [col1, col2, col3][i % 3]:
                    is_checked = column in st.session_state.renewable_selections
                    if st.checkbox(column.replace('generation ', '').title(), 
                                 value=is_checked, 
                                 key=f"renewable_{i}"):
                        if column not in st.session_state.renewable_selections:
                            st.session_state.renewable_selections.append(column)
                    else:
                        if column in st.session_state.renewable_selections:
                            st.session_state.renewable_selections.remove(column)
        else:
            # For more than 6 columns, use 4 columns
            col1, col2, col3, col4 = st.columns(4)
            
            for i, column in enumerate(available_columns):
                with [col1, col2, col3, col4][i % 4]:
                    is_checked = column in st.session_state.renewable_selections
                    if st.checkbox(column.replace('generation ', '').title(), 
                                 value=is_checked, 
                                 key=f"renewable_{i}"):
                        if column not in st.session_state.renewable_selections:
                            st.session_state.renewable_selections.append(column)
                    else:
                        if column in st.session_state.renewable_selections:
                            st.session_state.renewable_selections.remove(column)
        
        selected_columns = st.session_state.renewable_selections
        
        if not selected_columns:
            st.warning("⚠️ Please select at least one energy source to analyze.")
            st.stop()
        
        # Filter data by date range
        mask = (renewable_df['Date'] >= pd.to_datetime(start_date)) & (renewable_df['Date'] <= pd.to_datetime(end_date))
        filtered_df = renewable_df.loc[mask]
        
        # Create visualizations
        if chart_type == "Line Chart":
            fig = go.Figure()
            
            for column in selected_columns:
                fig.add_trace(go.Scatter(
                    x=filtered_df['Date'],
                    y=filtered_df[column],
                    mode='lines',
                    name=column.replace('generation ', '').title(),
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title=f'Renewable Energy Generation - {time_resolution} ({chart_type})',
                xaxis_title='Time',
                yaxis_title='Generation (MW)',
                template='plotly_dark',
                hovermode='x unified'
            )
            
        elif chart_type == "Stacked Area Chart":
            fig = go.Figure()
            
            # Define colors for the stacked area chart
            colors = px.colors.qualitative.Set3
            
            for i, column in enumerate(selected_columns):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Date'],
                    y=filtered_df[column],
                    mode='lines',
                    stackgroup='one',
                    name=column.replace('generation ', '').title(),
                    line=dict(width=0),
                    fillcolor=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                title=f'Renewable Energy Generation - {time_resolution} (Stacked Area)',
                xaxis_title='Time',
                yaxis_title='Generation (MW)',
                template='plotly_dark'
            )
            
        else:  # Pie Chart
            # Calculate total generation for each selected column
            totals = []
            labels = []
            
            for column in selected_columns:
                total = filtered_df[column].sum()
                totals.append(total)
                labels.append(column.replace('generation ', '').title())
            
            fig = px.pie(
                values=totals,
                names=labels,
                title=f'Renewable Energy Mix - {time_resolution}'
            )
            fig.update_layout(template='plotly_dark')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown('<h3 class="section-header">📊 Summary Statistics</h3>', unsafe_allow_html=True)
        with st.expander("📈 View Summary Statistics", expanded=True):
            cols = st.columns(len(selected_columns))
            for i, column in enumerate(selected_columns):
                with cols[i]:
                    avg_generation = filtered_df[column].mean()
                    total_generation = filtered_df[column].sum()
                    max_generation = filtered_df[column].max()
                    min_generation = filtered_df[column].min()
                    st.markdown(f"""
                    <div style='background: #23272f; border: 1px solid #2d323b; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
                        <div style='text-align: center; font-size: 1.1rem; color: #f5f6fa; font-weight: 600; margin-bottom: 0.5rem;'>
                            {column.replace('generation ', '').replace('generation fossil ', '').title()}
                        </div>
                        <div style='display: flex; justify-content: space-between;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{avg_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Avg</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{total_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Total</span>
                            </div>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-top: 0.5rem;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Max</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{max_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Min</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{min_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif analysis_type == "Non-Renewables":
        st.markdown('<h2 class="section-header">🏭 Non-Renewable Energy Analysis</h2>', unsafe_allow_html=True)
        
        # Chart type selection
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox("Chart Type:", ["Line Chart", "Stacked Area Chart", "Pie Chart"], key="nonrenewable_chart")
        with col2:
            time_resolution = st.selectbox("Time Resolution:", ["Daily", "Weekly", "Monthly"], key="nonrenewable_time")
        
        # Get the appropriate dataset and convert time to Date
        if time_resolution == "Daily":
            nonrenewable_df = energy_data['daily_nonrenewable']
            # Date column already created in load_energy_data()
        elif time_resolution == "Weekly":
            nonrenewable_df = energy_data['weekly_nonrenewable']
            # Convert weekly time format (e.g., "2015-W01") to datetime
            def parse_iso_week(week_str):
                year, week = week_str.split('-W')
                # Create a datetime for the first day of the year, then add weeks
                first_day = pd.Timestamp(year=int(year), month=1, day=1)
                # Find the first Monday of the year
                while first_day.weekday() != 0:  # Monday is 0
                    first_day += pd.Timedelta(days=1)
                # Add the weeks
                return first_day + pd.Timedelta(weeks=int(week)-1)
            
            nonrenewable_df['Date'] = nonrenewable_df['time'].apply(parse_iso_week)
        else:  # Monthly
            nonrenewable_df = energy_data['monthly_nonrenewable']
            # Convert monthly time format (e.g., "2015-01") to datetime
            nonrenewable_df['Date'] = pd.to_datetime(nonrenewable_df['time'] + '-01', format='%Y-%m-%d')
        
        # Column selection
        st.markdown('<h3 class="section-header">📋 Select Energy Sources</h3>', unsafe_allow_html=True)
        
        # Filter columns that exist in the dataset
        available_columns = [col for col in NONRENEWABLE_COLUMNS if col in nonrenewable_df.columns]
        
        if not available_columns:
            st.error("❌ No non-renewable energy columns found in the dataset.")
            st.stop()
        
        # Initialize session state for selections
        if 'nonrenewable_selections' not in st.session_state:
            st.session_state.nonrenewable_selections = []
        
        # Add Select All and Clear All buttons
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to move buttons down
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Select All", key="select_all_nonrenewable"):
                st.session_state.nonrenewable_selections = available_columns.copy()
                st.rerun()
        with col2:
            if st.button("Clear All", key="clear_all_nonrenewable"):
                st.session_state.nonrenewable_selections = []
                st.rerun()
        with col3:
            pass  # Empty column for symmetry
        with col4:
            pass  # Empty column for symmetry
        
        # Use a more organized grid layout for checkboxes
        if len(available_columns) <= 6:
            # For 6 or fewer columns, use 3 columns
            col1, col2, col3 = st.columns(3)
            
            for i, column in enumerate(available_columns):
                with [col1, col2, col3][i % 3]:
                    is_checked = column in st.session_state.nonrenewable_selections
                    if st.checkbox(column.replace('generation fossil ', '').title(), 
                                 value=is_checked, 
                                 key=f"nonrenewable_{i}"):
                        if column not in st.session_state.nonrenewable_selections:
                            st.session_state.nonrenewable_selections.append(column)
                    else:
                        if column in st.session_state.nonrenewable_selections:
                            st.session_state.nonrenewable_selections.remove(column)
        else:
            # For more than 6 columns, use 4 columns
            col1, col2, col3, col4 = st.columns(4)
            
            for i, column in enumerate(available_columns):
                with [col1, col2, col3, col4][i % 4]:
                    is_checked = column in st.session_state.nonrenewable_selections
                    if st.checkbox(column.replace('generation fossil ', '').title(), 
                                 value=is_checked, 
                                 key=f"nonrenewable_{i}"):
                        if column not in st.session_state.nonrenewable_selections:
                            st.session_state.nonrenewable_selections.append(column)
                    else:
                        if column in st.session_state.nonrenewable_selections:
                            st.session_state.nonrenewable_selections.remove(column)
        
        selected_columns = st.session_state.nonrenewable_selections
        
        if not selected_columns:
            st.warning("⚠️ Please select at least one energy source to analyze.")
            st.stop()
        
        # Filter data by date range
        mask = (nonrenewable_df['Date'] >= pd.to_datetime(start_date)) & (nonrenewable_df['Date'] <= pd.to_datetime(end_date))
        filtered_df = nonrenewable_df.loc[mask]
        
        # Create visualizations
        if chart_type == "Line Chart":
            fig = go.Figure()
            
            for column in selected_columns:
                fig.add_trace(go.Scatter(
                    x=filtered_df['Date'],
                    y=filtered_df[column],
                    mode='lines',
                    name=column.replace('generation fossil ', '').title(),
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title=f'Non-Renewable Energy Generation - {time_resolution} ({chart_type})',
                xaxis_title='Time',
                yaxis_title='Generation (MW)',
                template='plotly_dark',
                hovermode='x unified'
            )
            
        elif chart_type == "Stacked Area Chart":
            fig = go.Figure()
            
            # Define colors for the stacked area chart
            colors = px.colors.qualitative.Set3
            
            for i, column in enumerate(selected_columns):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Date'],
                    y=filtered_df[column],
                    mode='lines',
                    stackgroup='one',
                    name=column.replace('generation fossil ', '').title(),
                    line=dict(width=0),
                    fillcolor=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                title=f'Non-Renewable Energy Generation - {time_resolution} (Stacked Area)',
                xaxis_title='Time',
                yaxis_title='Generation (MW)',
                template='plotly_dark'
            )
            
        else:  # Pie Chart
            # Calculate total generation for each selected column
            totals = []
            labels = []
            
            for column in selected_columns:
                total = filtered_df[column].sum()
                totals.append(total)
                labels.append(column.replace('generation fossil ', '').title())
            
            fig = px.pie(
                values=totals,
                names=labels,
                title=f'Non-Renewable Energy Mix - {time_resolution}'
            )
            fig.update_layout(template='plotly_dark')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown('<h3 class="section-header">📊 Summary Statistics</h3>', unsafe_allow_html=True)
        with st.expander("📈 View Summary Statistics", expanded=True):
            cols = st.columns(len(selected_columns))
            for i, column in enumerate(selected_columns):
                with cols[i]:
                    avg_generation = filtered_df[column].mean()
                    total_generation = filtered_df[column].sum()
                    max_generation = filtered_df[column].max()
                    min_generation = filtered_df[column].min()
                    st.markdown(f"""
                    <div style='background: #23272f; border: 1px solid #2d323b; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
                        <div style='text-align: center; font-size: 1.1rem; color: #f5f6fa; font-weight: 600; margin-bottom: 0.5rem;'>
                            {column.replace('generation fossil ', '').replace('generation ', '').title()}
                        </div>
                        <div style='display: flex; justify-content: space-between;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{avg_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Avg</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{total_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Total</span>
                            </div>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-top: 0.5rem;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Max</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{max_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Min</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{min_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:  # Fossil Fuel Dependency
        st.markdown('<h2 class="section-header">🛢️ Fossil Fuel Dependency Analysis</h2>', unsafe_allow_html=True)
        
        # Chart type selection
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox("Chart Type:", ["Bar Chart", "Pie Chart", "Heatmap"], key="fossil_chart")
        with col2:
            analysis_type = st.selectbox("Analysis Type:", ["Dependency Percentages", "Average Values", "Count Analysis"], key="fossil_analysis")
        
        # Get the fossil fuel dependency dataset
        fossil_df = energy_data['fossil_fuel_dependency']
        
        # Column selection based on analysis type
        st.markdown('<h3 class="section-header">📋 Select Metrics</h3>', unsafe_allow_html=True)
        
        if analysis_type == "Dependency Percentages":
            available_columns = ['fossilDependencyPercent', 'brownCoalPercent', 'coalGasPercent', 
                               'naturalGasPercent', 'hardCoalPercent', 'oilPercent']
            display_names = ['Fossil Dependency %', 'Brown Coal %', 'Coal Gas %', 
                           'Natural Gas %', 'Hard Coal %', 'Oil %']
        elif analysis_type == "Average Values":
            available_columns = ['avgLoad', 'avgTotalFossil', 'avgTotalGeneration', 
                               'avgBrownCoal', 'avgCoalGas', 'avgNaturalGas', 'avgHardCoal', 'avgOil', 'avgOilShale', 'avgPeat']
            display_names = ['Avg Load', 'Avg Total Fossil', 'Avg Total Generation', 
                           'Avg Brown Coal', 'Avg Coal Gas', 'Avg Natural Gas', 'Avg Hard Coal', 'Avg Oil', 'Avg Oil Shale', 'Avg Peat']
        else:  # Count Analysis
            available_columns = ['count']
            display_names = ['Data Count']
        
        # Filter columns that exist in the dataset
        existing_columns = [col for col in available_columns if col in fossil_df.columns]
        existing_display_names = [display_names[i] for i, col in enumerate(available_columns) if col in fossil_df.columns]
        
        if not existing_columns:
            st.error("❌ No fossil fuel dependency columns found in the dataset.")
            st.stop()
        
        # Initialize session state for selections
        if 'fossil_selections' not in st.session_state:
            st.session_state.fossil_selections = []
        
        # Add Select All and Clear All buttons
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to move buttons down
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Select All", key="select_all_fossil"):
                st.session_state.fossil_selections = existing_columns.copy()
                st.rerun()
        with col2:
            if st.button("Clear All", key="clear_all_fossil"):
                st.session_state.fossil_selections = []
                st.rerun()
        with col3:
            pass  # Empty column for symmetry
        with col4:
            pass  # Empty column for symmetry
        
        # Use a more organized grid layout for checkboxes
        if len(existing_columns) <= 6:
            # For 6 or fewer columns, use 3 columns
            col1, col2, col3 = st.columns(3)
            
            for i, (column, display_name) in enumerate(zip(existing_columns, existing_display_names)):
                with [col1, col2, col3][i % 3]:
                    is_checked = column in st.session_state.fossil_selections
                    if st.checkbox(display_name, 
                                 value=is_checked, 
                                 key=f"fossil_{i}"):
                        if column not in st.session_state.fossil_selections:
                            st.session_state.fossil_selections.append(column)
                    else:
                        if column in st.session_state.fossil_selections:
                            st.session_state.fossil_selections.remove(column)
        else:
            # For more than 6 columns, use 4 columns
            col1, col2, col3, col4 = st.columns(4)
            
            for i, (column, display_name) in enumerate(zip(existing_columns, existing_display_names)):
                with [col1, col2, col3, col4][i % 4]:
                    is_checked = column in st.session_state.fossil_selections
                    if st.checkbox(display_name, 
                                 value=is_checked, 
                                 key=f"fossil_{i}"):
                        if column not in st.session_state.fossil_selections:
                            st.session_state.fossil_selections.append(column)
                    else:
                        if column in st.session_state.fossil_selections:
                            st.session_state.fossil_selections.remove(column)
        
        selected_columns = st.session_state.fossil_selections
        
        if not selected_columns:
            st.warning("⚠️ Please select at least one metric to analyze.")
            st.stop()
        
        # Create visualizations
        if chart_type == "Bar Chart":
            fig = go.Figure()
            
            for column in selected_columns:
                display_name = existing_display_names[existing_columns.index(column)]
                fig.add_trace(go.Bar(
                    x=fossil_df['time'],
                    y=fossil_df[column],
                    name=display_name,
                    text=fossil_df[column].round(2),
                    textposition='auto'
                ))
            
            fig.update_layout(
                title=f'Fossil Fuel Dependency - {analysis_type} (Bar Chart)',
                xaxis_title='Season & Load Level',
                yaxis_title='Value',
                template='plotly_dark',
                barmode='group'
            )
            
        elif chart_type == "Pie Chart":
            # Calculate average values across all seasons for each selected column
            fig = go.Figure()
            
            for column in selected_columns:
                display_name = existing_display_names[existing_columns.index(column)]
                avg_value = fossil_df[column].mean()
                
                fig.add_trace(go.Pie(
                    labels=[display_name],
                    values=[avg_value],
                    name=display_name,
                    hole=0.3
                ))
            
            fig.update_layout(
                title=f'Average Fossil Fuel Dependency - {analysis_type}',
                template='plotly_dark'
            )
            
        else:  # Heatmap
            # Create a heatmap of selected columns across all time periods
            heatmap_data = fossil_df[selected_columns].values
            heatmap_labels = [existing_display_names[existing_columns.index(col)] for col in selected_columns]
            
            # Convert to numpy array and round the values
            heatmap_data_np = np.array(heatmap_data)
            heatmap_data_rounded = np.round(heatmap_data_np, 2)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data_rounded,
                x=heatmap_labels,
                y=fossil_df['time'],
                colorscale='Viridis',
                text=heatmap_data_rounded,
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title=f'Fossil Fuel Dependency Heatmap - {analysis_type}',
                xaxis_title='Metrics',
                yaxis_title='Season & Load Level',
                template='plotly_dark'
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.markdown('<h3 class="section-header">📊 Summary Statistics</h3>', unsafe_allow_html=True)
        with st.expander("📈 View Summary Statistics", expanded=True):
            cols = st.columns(len(selected_columns))
            for i, column in enumerate(selected_columns):
                with cols[i]:
                    avg_generation = fossil_df[column].mean()
                    total_generation = fossil_df[column].sum()
                    max_generation = fossil_df[column].max()
                    min_generation = fossil_df[column].min()
                    display_name = existing_display_names[existing_columns.index(column)]
                    st.markdown(f"""
                    <div style='background: #23272f; border: 1px solid #2d323b; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
                        <div style='text-align: center; font-size: 1.1rem; color: #f5f6fa; font-weight: 600; margin-bottom: 0.5rem;'>
                            {display_name}
                        </div>
                        <div style='display: flex; justify-content: space-between;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{avg_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Avg</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 1.2rem; color: #00b894; font-weight: bold;'>{total_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>Total</span>
                            </div>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-top: 0.5rem;'>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Max</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{max_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                            <div style='text-align: center;'>
                                <span style='font-size: 0.9rem; color: #f5f6fa; font-weight: 500;'>Min</span><br>
                                <span style='font-size: 0.8rem; color: #b2bec3;'>{min_generation:.2f}</span>
                                <span style='font-size: 0.7rem; color: #b2bec3; margin-left: 2px;'>MWh</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ML ANALYSIS PAGE
elif page == "👾 ML Analysis":
    st.markdown('<h1 class="main-header">👾 Machine Learning Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
<h2>Vision for an Intelligent Grid</h2>
<ul>
    <li>Autonomous system capable of <strong>real-time monitoring and forecasting</strong>.</li>
    <li>Dynamically balances energy supply by:
        <ul>
            <li>Predicting shortfalls in renewable energy</li>
            <li>Seamlessly switching to backup sources</li>
        </ul>
    </li>
    <li>Optimizes for:
        <ul>
            <li>Cost efficiency</li>
            <li>Reduced carbon emissions</li>
            <li>Grid reliability</li>
        </ul>
    </li>
    <li>Utilizes <strong>machine learning</strong> and data-driven algorithms to continuously enhance decision-making.</li>
</ul>

<h3>Current Gaps</h3>
<ul>
    <li>Lack of <strong>adaptive, predictive, and automated control systems</strong>.</li>
    <li>Existing systems are reactive and manual, failing to:
        <ul>
            <li>Anticipate renewable variability</li>
            <li>Make proactive adjustments</li>
        </ul>
    </li>
    <li>Results in:
        <ul>
            <li>Operational inefficiencies</li>
            <li>Higher carbon emissions</li>
            <li>Increased risk of outages</li>
        </ul>
    </li>
    <li>Hinders progress toward a <strong>sustainable and reliable energy future</strong>.</li>
</ul>
""", unsafe_allow_html=True)
    
    # Forecast selection
    st.markdown('<h2 class="section-header">🔮 Forecast Selection</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        forecast_type = st.selectbox(
            "Choose Forecast Type:",
            ["Load Forecast"],
            # ["Load Forecast", "Renewable Generation Forecast", "Peak Demand Forecast", "Seasonal Forecast"]
        )
    
    with col2:
        metric_type = st.selectbox(
            "Select Metrics:",
            ["RMSE", "MAE", "MAPE", "R²", "All Metrics"]
        )
    
    # Time range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2015, 1, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2018, 12, 31))
    
    # Validate date range for ML Analysis
    min_date = datetime(2015, 1, 1).date()
    max_date = datetime(2018, 12, 31).date()
    
    if start_date < min_date or end_date > max_date or start_date > max_date or end_date < min_date:
        st.markdown("""
        <div style="background-color: #ff4444; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>⚠️ Invalid Date Range</strong><br>
            Please choose dates between <strong>01/01/2015</strong> and <strong>31/12/2018</strong>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Validate that start_date is before end_date
    if start_date >= end_date:
        st.markdown("""
        <div style="background-color: #ff4444; color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <strong>⚠️ Invalid Date Range</strong><br>
            Start date must be <strong>before</strong> end date
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Filter data based on date range
    # mask = (ml_load_data['Date'] >= pd.to_datetime(start_date)) & (ml_load_data['Date'] <= pd.to_datetime(end_date))
    # filtered_data = ml_load_data

    # ml_load_data['Date'] = pd.to_datetime(ml_load_data['Date'], format='%d-%m-%y')
    # ml_load_data = ml_load_data.sort_values('Date')
    # filtered_data = ml_load_data  # (or your filtered version)

    ml_load_data['Date'] = pd.to_datetime(ml_load_data['Date'], format='%d-%m-%y')
    ml_load_data = ml_load_data.sort_values('Date')

    mask = (ml_load_data['Date'] >= pd.to_datetime(start_date)) & (ml_load_data['Date'] <= pd.to_datetime(end_date))
    filtered_data = ml_load_data.loc[mask]
    
    # Actual vs Predicted Plot
    st.markdown('<h2 class="section-header">📈 Actual vs Predicted Analysis</h2>', unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Actual vs Predicted Load', 'Prediction Error'),
        vertical_spacing=0.1
    )
    
    # Main plot
    fig.add_trace(
        go.Scatter(x=filtered_data['Date'], y=filtered_data['Actual_Load'], 
                  name='Actual Load', line=dict(color='#1f77b4', width=2)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=filtered_data['Date'], y=filtered_data['Predicted_Load'], 
                  name='Predicted Load', line=dict(color='#ff7f0e', width=2)),
        row=1, col=1
    )
    
    # Error plot
    error = filtered_data['Actual_Load'] - filtered_data['Predicted_Load']
    fig.add_trace(
        go.Scatter(x=filtered_data['Date'], y=error, 
                  name='Prediction Error', line=dict(color='#d62728', width=1)),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        template='plotly_dark',
        title_text=f"{forecast_type} - Performance Analysis",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics display
    st.markdown('<h2 class="section-header">📊 Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    rmse = np.sqrt(np.mean((filtered_data['Actual_Load'] - filtered_data['Predicted_Load'])**2))
    mae = np.mean(np.abs(filtered_data['Actual_Load'] - filtered_data['Predicted_Load']))
    mape = np.mean(np.abs((filtered_data['Actual_Load'] - filtered_data['Predicted_Load']) / filtered_data['Actual_Load'])) * 100
    r2 = np.corrcoef(filtered_data['Actual_Load'], filtered_data['Predicted_Load'])[0,1]**2
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("RMSE", f"{rmse:.2f}", "MWh")
    with col2:
        st.metric("MAE", f"{mae:.2f}", "MWh")
    with col3:
        st.metric("MAPE", f"{mape:.2f}", "%")
    with col4:
        st.metric("R² Score", f"{r2:.3f}", "")
    
    # # Correlation Matrix
    # st.markdown('<h2 class="section-header">🔗 Correlation Matrix</h2>', unsafe_allow_html=True)
    
    # corr_data = filtered_data[['Actual_Load', 'Predicted_Load', 'Temperature', 'Humidity']].corr()
    
    # fig_corr = px.imshow(
    #     corr_data,
    #     text_auto=True,
    #     aspect="auto",
    #     color_continuous_scale='RdBu_r',
    #     title="Feature Correlation Matrix"
    # )
    # fig_corr.update_layout(template='plotly_dark')
    # st.plotly_chart(fig_corr, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>⚡ Energy Analysis & Forecasting Platform | Built with Streamlit</p>
    <p>📊 Advanced Analytics • 👾 Machine Learning • 🌱 Sustainable Energy</p>
</div>
""", unsafe_allow_html=True)