import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="centered",
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
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">⚡ Energy Consumption Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculate your daily energy usage based on your home setup</div>', unsafe_allow_html=True)

# Energy consumption rates (kWh)
ENERGY_RATES = {
    'light': 0.4,
    'fan': 0.8,
    'ac': 3,
    'fridge': 4,
    'washing_machine': 2
}

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
        
        # Calculate button
        if st.button("🔍 Calculate Energy Consumption", type="primary", use_container_width=True):
            if name and age and city and area:
                # Calculate energy consumption
                energy_consumption = 0
                
                # Base consumption (lights and fans)
                if bhk_type == "1BHK":
                    energy_consumption = ENERGY_RATES['light'] * 2 + ENERGY_RATES['fan'] * 2
                elif bhk_type == "2BHK":
                    energy_consumption = ENERGY_RATES['light'] * 3 + ENERGY_RATES['fan'] * 3
                elif bhk_type == "3BHK":
                    energy_consumption = ENERGY_RATES['light'] * 4 + ENERGY_RATES['fan'] * 4
                
                # Add appliances
                if has_ac == "Yes":
                    energy_consumption += ENERGY_RATES['ac']
                if has_fridge == "Yes":
                    energy_consumption += ENERGY_RATES['fridge']
                if has_washing_machine == "Yes":
                    energy_consumption += ENERGY_RATES['washing_machine']
                
                # Display results
                st.markdown("---")
                st.markdown(f"<div class='result-box'><div class='result-main'>{energy_consumption} kWh</div><div class='result-sub'>Daily Energy Consumption</div></div>", unsafe_allow_html=True)
                
                # Additional calculations
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Daily Usage", f"{energy_consumption} kWh")
                
                with col2:
                    monthly_consumption = energy_consumption * 30
                    st.metric("Monthly Usage", f"{monthly_consumption:.1f} kWh")
                
                with col3:
                    yearly_consumption = energy_consumption * 365
                    st.metric("Yearly Usage", f"{yearly_consumption:.1f} kWh")
                
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
                
                # Energy breakdown
                st.markdown("### 📊 Energy Breakdown")
                breakdown_data = {}
                
                if bhk_type == "1BHK":
                    breakdown_data["Lights"] = ENERGY_RATES['light'] * 2
                    breakdown_data["Fans"] = ENERGY_RATES['fan'] * 2
                elif bhk_type == "2BHK":
                    breakdown_data["Lights"] = ENERGY_RATES['light'] * 3
                    breakdown_data["Fans"] = ENERGY_RATES['fan'] * 3
                elif bhk_type == "3BHK":
                    breakdown_data["Lights"] = ENERGY_RATES['light'] * 4
                    breakdown_data["Fans"] = ENERGY_RATES['fan'] * 4
                
                if has_ac == "Yes":
                    breakdown_data["AC"] = ENERGY_RATES['ac']
                if has_fridge == "Yes":
                    breakdown_data["Refrigerator"] = ENERGY_RATES['fridge']
                if has_washing_machine == "Yes":
                    breakdown_data["Washing Machine"] = ENERGY_RATES['washing_machine']
                
                # Display breakdown as a bar chart
                st.bar_chart(breakdown_data)
                
                # Energy saving tips
                st.markdown("### 💡 Energy Saving Tips")
                tips = [
                    "Use LED bulbs instead of incandescent bulbs",
                    "Set AC temperature to 24°C or higher",
                    "Use fans along with AC to circulate air better",
                    "Unplug appliances when not in use",
                    "Use washing machine with full loads",
                    "Regular maintenance of appliances improves efficiency"
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
        💡 Energy Consumption Calculator | Calculate your daily energy usage
    </div>
    """,
    unsafe_allow_html=True
)

# Instructions for running the app
st.sidebar.markdown("""
### 📋 How to Run This App

1. **Install Streamlit:**
   ```bash
   pip install streamlit
   ```

2. **Save this code** as `energy_calculator.py`

3. **Run the app:**
   ```bash
   streamlit run energy_calculator.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

### ⚡ Features:
- Interactive form with validation
- Real-time energy consumption calculation
- Visual breakdown of energy usage
- Energy saving tips
- Responsive design
- Clean, modern interface
""")