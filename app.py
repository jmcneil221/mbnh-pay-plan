import streamlit as st
from pay_plan import MauroMotorsPayPlan

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Monthly Bonus Calculator", page_icon="🚙", layout="centered")

# --- CUSTOM HEADER ---
st.markdown("<h2 style='text-align: center;'>Monthly Bonus Calculator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d; font-style: italic;'>Engineered by Simply J Labs</p>", unsafe_allow_html=True)
st.divider()

# --- INPUT SECTION (Simple & Intuitve) ---
st.subheader("📊 1. Monthly Performance")
st.caption("Adjust the sliders and inputs below to calculate your estimated pay.")

col1, col2 = st.columns(2)
with col1:
    new_units = st.number_input("New Cars Sold", min_value=0, value=6, step=1)
    used_units = st.number_input("Used Cars Sold", min_value=0, value=6, step=1)
    rolling_avg = st.number_input("3-Mo Rolling Avg", min_value=0, value=15, step=1)
with col2:
    total_fi_gross = st.number_input("Total F&I Gross ($)", min_value=0, value=18000, step=500)
    # Using sliders for percentages makes it much easier for mobile users
    security_pen = st.slider("Security Guard %", min_value=0, max_value=100, value=55, format="%d%%")
    zurich_pen = st.slider("Zurich Shield %", min_value=0, max_value=100, value=40, format="%d%%")

# --- INSTANTIATE LOGIC ---
calc = MauroMotorsPayPlan(
    new_units=new_units, used_units=used_units, rolling_3_mo_avg=rolling_avg,
    total_f_and_i_gross=total_fi_gross, security_pen=security_pen, zurich_pen=zurich_pen
)

flats = calc.get_mini_flats()
volume_bonus = calc.calculate_volume_bonus()
fi_bonus = calc.calculate_f_and_i_bonus()
velocity_bonus = calc.calculate_new_car_velocity()
total_bonus = volume_bonus + fi_bonus + velocity_bonus

st.divider()

# --- RESULTS SECTION ---
st.subheader("💰 2. Pay Breakdown")

# Clean, modern metric tiles
c1, c2, c3 = st.columns(3)
c1.metric("Volume Bonus", f"${volume_bonus:,.0f}")
c2.metric("F&I Bonus", f"${fi_bonus:,.0f}")
c3.metric("Velocity Bonus", f"${velocity_bonus:,.0f}")

st.info(f"**Total Bonus Pay: ${total_bonus:,.0f}** \n*(Mini Flats: New ${flats['new_flat']} / Used ${flats['used_flat']})*")

st.divider()

# --- THE "WOW" FACTOR: SMART INSIGHTS ENGINE ---
st.subheader("🧠 Simply J Labs: Smart Insights")
st.caption("Actionable intel to maximize your paycheck.")

insights_found = False

# Insight 1: Volume Trapdoor
if calc.new_units < 5:
    st.error(f"🚨 **Volume Penalty Active:** You are currently losing 50% of your Volume Bonus. **Action:** Sell {5 - calc.new_units} more New Car(s) to restore full payout!")
    insights_found = True

# Insight 2: Total Units Minimums
if calc.total_units < 10:
    st.warning(f"⚠️ **Bonus Minimums Not Met:** You need {10 - calc.total_units} more total unit(s) to qualify for the F&I and Velocity bonuses.")
    insights_found = True

# Insight 3: F&I Penetration Trapdoor
if calc.total_units >= 10:
    if calc.security_pen < 50 or calc.zurich_pen < 35:
        issues = []
        if calc.security_pen < 50: issues.append(f"Security to 50% (currently {calc.security_pen}%)")
        if calc.zurich_pen < 35: issues.append(f"Zurich to 35% (currently {calc.zurich_pen}%)")
        st.error(f"🚨 **F&I Penalty Active:** You are losing 25% of your F&I Bonus. **Action:** Raise your {' and '.join(issues)} to recover those funds.")
        insights_found = True
    else:
        st.success("✅ **F&I Penetration:** Great job! You are above the 50% Security and 35% Zurich thresholds. Your F&I bonus is fully protected.")
        insights_found = True

# Insight 4: Positive reinforcement if they are crushing it
if not insights_found and calc.total_units >= 10 and calc.new_units >= 5:
    st.success("🎯 **Maximized!** You are successfully avoiding all penalty trapdoors. Keep pushing your rolling average to unlock the next volume tier!")
