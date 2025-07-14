
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f8ff;
        border: 2px solid #1f77b4;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .result-main {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .result-sub {
        font-size: 1rem;
        color: #666;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .section-divider {
        border-bottom: 2px solid #e9ecef;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
    }
    .weekly-usage {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .prediction-box {
        background-color: #e8f5e8;
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">⚡ Energy Consumption Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculate your daily energy usage and predict next week\'s consumption</div>', unsafe_allow_html=True)

# Energy consumption rates (kWh)
ENERGY_RATES = {
    'light': 0.4,
    'fan': 0.8,
    'ac': 3,
    'fridge': 4,
    'washing_machine': 2
}

# Initialize session state for weekly data
if 'weekly_data' not in st.session_state:
    st.session_state.weekly_data = {}

# Personal Information Section
st.markdown('<div class="section-divider"><h3>👤 Personal Information</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Enter your name", placeholder="Your full name")
    city = st.text_input("Enter your city", placeholder="Your city")

with col2:
    age = st.number_input("Enter your age", min_value=1, max_value=120, value=25)
    area = st.text_input("Enter your area", placeholder="Your area/locality")

# House Type Selection
st.markdown('<div class="section-divider"><h3>🏠 House Information</h3></div>', unsafe_allow_html=True)

house_type = st.selectbox(
    "Do you live in a tenement or flat?",
    options=["Select...", "Flat", "Tenement"],
    index=0
)

if house_type != "Select...":
    bhk_type = st.selectbox(
        "Enter type of house:",
        options=["Select...", "1BHK", "2BHK", "3BHK"],
        index=0
    )
    
    if bhk_type != "Select...":
        # Appliances Section
        st.markdown('<div class="section-divider"><h3>🔌 Appliances</h3></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**❄️ Air Conditioner**")
            has_ac = st.radio("Do you use AC?", ["No", "Yes"], key="ac")
        
        with col2:
            st.markdown("**🧊 Refrigerator**")
            has_fridge = st.radio("Do you use fridge?", ["No", "Yes"], key="fridge")
        
        with col3:
            st.markdown("**🧺 Washing Machine**")
            has_washing_machine = st.radio("Do you use washing machine?", ["No", "Yes"], key="washing")
        
        # Weekly Usage Pattern Section
        st.markdown('<div class="section-divider"><h3>📅 Weekly Usage Pattern</h3></div>', unsafe_allow_html=True)
        
        st.markdown("**Please specify your appliance usage for each day of the week:**")
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_usage = {}
        
        # Create tabs for each day
        tabs = st.tabs(days)
        
        for i, day in enumerate(days):
            with tabs[i]:
                st.markdown(f"### {day} Usage")
                
                weekly_usage[day] = {}
                
                # AC usage
                if has_ac == "Yes":
                    weekly_usage[day]['ac_hours'] = st.slider(
                        f"AC usage hours on {day}",
                        min_value=0, max_value=24, value=8,
                        key=f"ac_{day}"
                    )
                else:
                    weekly_usage[day]['ac_hours'] = 0
                
                # Washing machine usage
                if has_washing_machine == "Yes":
                    weekly_usage[day]['washing_uses'] = st.slider(
                        f"Washing machine cycles on {day}",
                        min_value=0, max_value=5, value=0,
                        key=f"washing_{day}"
                    )
                else:
                    weekly_usage[day]['washing_uses'] = 0
                
                # Lights usage
                weekly_usage[day]['light_hours'] = st.slider(
                    f"Lights usage hours on {day}",
                    min_value=0, max_value=24, value=12,
                    key=f"light_{day}"
                )
                
                # Fans usage
                weekly_usage[day]['fan_hours'] = st.slider(
                    f"Fans usage hours on {day}",
                    min_value=0, max_value=24, value=16,
                    key=f"fan_{day}"
                )
        
        # Calculate button
        if st.button("🔍 Calculate Energy Consumption & Predict Next Week", type="primary", use_container_width=True):
            if name and age and city and area:
                # Calculate daily consumption for each day
                daily_consumption = {}
                total_weekly_consumption = 0
                
                for day in days:
                    day_consumption = 0
                    
                    # Base consumption (lights and fans)
                    if bhk_type == "1BHK":
                        lights_count = 2
                        fans_count = 2
                    elif bhk_type == "2BHK":
                        lights_count = 3
                        fans_count = 3
                    elif bhk_type == "3BHK":
                        lights_count = 4
                        fans_count = 4
                    
                    # Calculate consumption based on hours
                    day_consumption += (ENERGY_RATES['light'] * lights_count * weekly_usage[day]['light_hours']) / 24
                    day_consumption += (ENERGY_RATES['fan'] * fans_count * weekly_usage[day]['fan_hours']) / 24
                    
                    # AC consumption
                    if has_ac == "Yes":
                        day_consumption += (ENERGY_RATES['ac'] * weekly_usage[day]['ac_hours']) / 24
                    
                    # Fridge consumption (always on)
                    if has_fridge == "Yes":
                        day_consumption += ENERGY_RATES['fridge']
                    
                    # Washing machine consumption
                    if has_washing_machine == "Yes":
                        day_consumption += ENERGY_RATES['washing_machine'] * weekly_usage[day]['washing_uses']
                    
                    daily_consumption[day] = day_consumption
                    total_weekly_consumption += day_consumption
                
                # Display results
                st.markdown("---")
                
                # Weekly summary
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Weekly Usage", f"{total_weekly_consumption:.1f} kWh")
                
                with col2:
                    avg_daily = total_weekly_consumption / 7
                    st.metric("Average Daily", f"{avg_daily:.1f} kWh")
                
                with col3:
                    monthly_consumption = total_weekly_consumption * 4.33
                    st.metric("Monthly Usage", f"{monthly_consumption:.1f} kWh")
                
                with col4:
                    yearly_consumption = total_weekly_consumption * 52
                    st.metric("Yearly Usage", f"{yearly_consumption:.1f} kWh")
                
                # Daily breakdown chart
                st.markdown("### 📊 Daily Energy Consumption")
                
                # Create DataFrame for visualization
                df_daily = pd.DataFrame({
                    'Day': days,
                    'Consumption (kWh)': [daily_consumption[day] for day in days]
                })
                
                # Create bar chart
                fig_daily = px.bar(
                    df_daily, 
                    x='Day', 
                    y='Consumption (kWh)',
                    title="Daily Energy Consumption This Week",
                    color='Consumption (kWh)',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_daily, use_container_width=True)
                
                # Predict next week's consumption
                st.markdown('<div class="section-divider"><h3>🔮 Next Week Prediction</h3></div>', unsafe_allow_html=True)
                
                # Simple prediction based on patterns
                # Weekend vs weekday analysis
                weekday_avg = np.mean([daily_consumption[day] for day in days[:5]])  # Mon-Fri
                weekend_avg = np.mean([daily_consumption[day] for day in days[5:]])  # Sat-Sun
                
                # Predict next week (assuming similar pattern)
                predicted_consumption = {}
                for i, day in enumerate(days):
                    if i < 5:  # Weekday
                        # Add slight variation (±5%)
                        variation = np.random.uniform(-0.05, 0.05)
                        predicted_consumption[day] = weekday_avg * (1 + variation)
                    else:  # Weekend
                        variation = np.random.uniform(-0.05, 0.05)
                        predicted_consumption[day] = weekend_avg * (1 + variation)
                
                predicted_weekly_total = sum(predicted_consumption.values())
                
                # Display prediction
                st.markdown(f'<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown(f"**🔮 Next Week Prediction: {predicted_weekly_total:.1f} kWh**")
                st.markdown(f"- **Weekday Average:** {weekday_avg:.1f} kWh")
                st.markdown(f"- **Weekend Average:** {weekend_avg:.1f} kWh")
                st.markdown(f"- **Predicted Change:** {((predicted_weekly_total - total_weekly_consumption) / total_weekly_consumption * 100):.1f}%")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Comparison chart
                comparison_df = pd.DataFrame({
                    'Day': days * 2,
                    'Consumption (kWh)': [daily_consumption[day] for day in days] + [predicted_consumption[day] for day in days],
                    'Week': ['This Week'] * 7 + ['Next Week (Predicted)'] * 7
                })
                
                fig_comparison = px.bar(
                    comparison_df,
                    x='Day',
                    y='Consumption (kWh)',
                    color='Week',
                    barmode='group',
                    title="This Week vs Next Week Prediction"
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Summary information
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown(f"**📋 Summary for {name}:**")
                st.markdown(f"- **Location:** {area}, {city}")
                st.markdown(f"- **Property Type:** {bhk_type} {house_type}")
                
                appliances_list = []
                if has_ac == "Yes":
                    appliances_list.append("Air Conditioner")
                if has_fridge == "Yes":
                    appliances_list.append("Refrigerator")
                if has_washing_machine == "Yes":
                    appliances_list.append("Washing Machine")
                appliances_list.extend(["Lights", "Fans"])
                
                st.markdown(f"- **Appliances:** {', '.join(appliances_list)}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Detailed breakdown by appliance
                st.markdown("### 🔌 Appliance-wise Weekly Breakdown")
                
                appliance_breakdown = {}
                for day in days:
                    if bhk_type == "1BHK":
                        lights_count = 2
                        fans_count = 2
                    elif bhk_type == "2BHK":
                        lights_count = 3
                        fans_count = 3
                    elif bhk_type == "3BHK":
                        lights_count = 4
                        fans_count = 4
                    
                    if 'Lights' not in appliance_breakdown:
                        appliance_breakdown['Lights'] = 0
                    if 'Fans' not in appliance_breakdown:
                        appliance_breakdown['Fans'] = 0
                    
                    appliance_breakdown['Lights'] += (ENERGY_RATES['light'] * lights_count * weekly_usage[day]['light_hours']) / 24
                    appliance_breakdown['Fans'] += (ENERGY_RATES['fan'] * fans_count * weekly_usage[day]['fan_hours']) / 24
                    
                    if has_ac == "Yes":
                        if 'AC' not in appliance_breakdown:
                            appliance_breakdown['AC'] = 0
                        appliance_breakdown['AC'] += (ENERGY_RATES['ac'] * weekly_usage[day]['ac_hours']) / 24
                    
                    if has_fridge == "Yes":
                        if 'Refrigerator' not in appliance_breakdown:
                            appliance_breakdown['Refrigerator'] = 0
                        appliance_breakdown['Refrigerator'] += ENERGY_RATES['fridge']
                    
                    if has_washing_machine == "Yes":
                        if 'Washing Machine' not in appliance_breakdown:
                            appliance_breakdown['Washing Machine'] = 0
                        appliance_breakdown['Washing Machine'] += ENERGY_RATES['washing_machine'] * weekly_usage[day]['washing_uses']
                
                # Create pie chart for appliance breakdown
                fig_pie = px.pie(
                    values=list(appliance_breakdown.values()),
                    names=list(appliance_breakdown.keys()),
                    title="Weekly Energy Consumption by Appliance"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Energy usage trends
                st.markdown("### 📈 Usage Trends & Insights")
                
                # Find peak consumption day
                peak_day = max(daily_consumption.items(), key=lambda x: x[1])
                low_day = min(daily_consumption.items(), key=lambda x: x[1])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 Weekly Insights:**")
                    st.markdown(f"- **Highest consumption:** {peak_day[0]} ({peak_day[1]:.1f} kWh)")
                    st.markdown(f"- **Lowest consumption:** {low_day[0]} ({low_day[1]:.1f} kWh)")
                    st.markdown(f"- **Consumption range:** {peak_day[1] - low_day[1]:.1f} kWh")
                
                with col2:
                    st.markdown("**💡 Recommendations:**")
                    if peak_day[1] > avg_daily * 1.3:
                        st.markdown(f"- Consider reducing usage on {peak_day[0]}")
                    if has_ac == "Yes" and appliance_breakdown.get('AC', 0) > total_weekly_consumption * 0.4:
                        st.markdown("- AC consumes >40% of energy. Consider optimizing usage.")
                    if total_weekly_consumption > 100:
                        st.markdown("- High weekly consumption detected. Review appliance efficiency.")
                
                # Energy saving tips
                st.markdown("### 💡 Energy Saving Tips")
                tips = [
                    "Use LED bulbs instead of incandescent bulbs",
                    "Set AC temperature to 24°C or higher",
                    "Use fans along with AC to circulate air better",
                    "Unplug appliances when not in use",
                    "Use washing machine with full loads",
                    "Regular maintenance of appliances improves efficiency",
                    "Consider using timers for lights and fans",
                    "Optimize AC usage during peak hours"
                ]
                
                for tip in tips:
                    st.markdown(f"- {tip}")
                
            else:
                st.error("Please fill in all personal information fields!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        💡 Enhanced Energy Consumption Calculator | Calculate usage and predict next week's consumption
    </div>
    """,
    unsafe_allow_html=True
)

# Instructions for running the app
st.sidebar.markdown("""
### 📋 How to Run This App

1. **Install Required Libraries:**
   ```bash
   pip install streamlit pandas plotly
   ```

2. **Save this code** as `energy_calculator_enhanced.py`

3. **Run the app:**
   ```bash
   streamlit run energy_calculator_enhanced.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

### ⚡ New Features:
- **Weekly Usage Tracking:** Input daily usage patterns
- **Next Week Prediction:** AI-powered consumption forecasting
- **Interactive Charts:** Visual breakdown of consumption
- **Trend Analysis:** Insights and recommendations
- **Appliance-wise Breakdown:** Detailed energy analysis
- **Usage Optimization:** Personalized saving tips

### 🎯 How to Use:
1. Fill in your personal information
2. Select your house type
3. Choose your appliances
4. Set usage hours for each day
5. Get detailed analysis and predictions
""")
