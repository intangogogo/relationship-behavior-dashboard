import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# -------------------------------------------------------------
# 1. Page Configuration & Setup
# -------------------------------------------------------------
st.set_page_config(
    page_title="Systemic Relational & Interaction Analytics",
    page_icon="🤝",
    layout="wide"
)

# -------------------------------------------------------------
# 2. Database Mapping Values (Weights for Systems Math)
# -------------------------------------------------------------
# Gottman Bid Response Weights (Turning Directions)
BID_WEIGHTS = {
    "Turn Toward (Validating/Responsive)": 1.0,
    "Turn Away (Ignoring/Dismissing)": -1.0,
    "Turn Against (Critical/Defensive)": -2.0
}

# EFT Space State Weights (Ps)
SPACE_WEIGHTS = {
    "Withdrawing": 1,
    "Neutral": 0,
    "Approaching": -1
}

# EFT Reaction Weights (Ur)
REACTION_WEIGHTS = {
    "Pursued Anxiously": 1,
    "Regulated & Gave Space": 0,
    "Withdrew in Retaliation": -1,
    "N/A": 0
}

# -------------------------------------------------------------
# 3. Session State Database Initialization (No Dating App Data)
# -------------------------------------------------------------
# DATABASE 1: Solo Self-Regulation & Readiness Logs
if 'self_reg_df' not in st.session_state:
    self_reg_mock = [
        {"Date": "2026-05-01", "Emotion": "Lonely", "Intensity": 7, "Somatic": "Chest", "Trigger": "Attachment Trigger", "Response": "Reactive", "Capacity_Hours": 3.0, "Loneliness_Drive": 8, "Boundary_Met": "No"},
        {"Date": "2026-05-03", "Emotion": "Anxious", "Intensity": 6, "Somatic": "Stomach", "Trigger": "Daily Stress", "Response": "Suppressed", "Capacity_Hours": 2.5, "Loneliness_Drive": 7, "Boundary_Met": "No"},
        {"Date": "2026-05-05", "Emotion": "Peaceful", "Intensity": 3, "Somatic": "None", "Trigger": "None", "Response": "Validated", "Capacity_Hours": 6.0, "Loneliness_Drive": 3, "Boundary_Met": "Yes"},
        {"Date": "2026-05-07", "Emotion": "Overwhelmed", "Intensity": 8, "Somatic": "Jaw", "Trigger": "Daily Stress", "Response": "Reactive", "Capacity_Hours": 2.0, "Loneliness_Drive": 8, "Boundary_Met": "No"},
        {"Date": "2026-05-09", "Emotion": "Secure", "Intensity": 4, "Somatic": "None", "Trigger": "None", "Response": "Validated", "Capacity_Hours": 8.0, "Loneliness_Drive": 2, "Boundary_Met": "Yes"},
        {"Date": "2026-05-11", "Emotion": "Resentful", "Intensity": 7, "Somatic": "Shoulders", "Trigger": "Boundary Crossed", "Response": "Suppressed", "Capacity_Hours": 4.0, "Loneliness_Drive": 5, "Boundary_Met": "No"},
        {"Date": "2026-05-13", "Emotion": "Secure", "Intensity": 3, "Somatic": "None", "Trigger": "None", "Response": "Validated", "Capacity_Hours": 10.0, "Loneliness_Drive": 2, "Boundary_Met": "Yes"}
    ]
    st.session_state.self_reg_df = pd.DataFrame(self_reg_mock)

# DATABASE 2: Expanded Interpersonal Interaction Logs (Including Gottman Metrics)
if 'interaction_df' not in st.session_state:
    interaction_mock = [
        {"Date": "2026-05-14", "Type": "Venting", "Vulnerability": 8, "Bid_Direction": "Turn Away (Ignoring/Dismissing)", "Horsemen": "None", "Repair_Attempt": "No Attempt", "My_State": "Lonely/Misunderstood", "Partner_Space": "Neutral", "My_Reaction": "Regulated & Gave Space"},
        {"Date": "2026-05-15", "Type": "Requesting Closeness", "Vulnerability": 7, "Bid_Direction": "Turn Away (Ignoring/Dismissing)", "Horsemen": "Stonewalling", "Repair_Attempt": "Failed", "My_State": "Anxious", "Partner_Space": "Withdrawing", "My_Reaction": "Pursued Anxiously"},
        {"Date": "2026-05-17", "Type": "Difficult Conversation", "Vulnerability": 9, "Bid_Direction": "Turn Toward (Validating/Responsive)", "Horsemen": "None", "Repair_Attempt": "Successful", "My_State": "Connected", "Partner_Space": "Approaching", "My_Reaction": "Regulated & Gave Space"},
        {"Date": "2026-05-19", "Type": "Venting", "Vulnerability": 6, "Bid_Direction": "Turn Against (Critical/Defensive)", "Horsemen": "Criticism", "Repair_Attempt": "No Attempt", "My_State": "Resentful", "Partner_Space": "Withdrawing", "My_Reaction": "Pursued Anxiously"},
        {"Date": "2026-05-20", "Type": "Venting", "Vulnerability": 8, "Bid_Direction": "Turn Toward (Validating/Responsive)", "Horsemen": "None", "Repair_Attempt": "Successful", "My_State": "Connected", "Partner_Space": "Neutral", "My_Reaction": "Regulated & Gave Space"},
        {"Date": "2026-05-21", "Type": "Difficult Conversation", "Vulnerability": 7, "Bid_Direction": "Turn Away (Ignoring/Dismissing)", "Horsemen": "Defensiveness", "Repair_Attempt": "Failed", "My_State": "Lonely/Misunderstood", "Partner_Space": "Withdrawing", "My_Reaction": "Regulated & Gave Space"}
    ]
    st.session_state.interaction_df = pd.DataFrame(interaction_mock)

df_self = st.session_state.self_reg_df
df_interact = st.session_state.interaction_df

# -------------------------------------------------------------
# 4. Math Processing Engine
# -------------------------------------------------------------
df_interact_proc = df_interact.copy()
df_interact_proc['Bid_Weight'] = df_interact_proc['Bid_Direction'].map(BID_WEIGHTS)
df_interact_proc['Ps_Weight'] = df_interact_proc['Partner_Space'].map(SPACE_WEIGHTS)
df_interact_proc['Ur_Weight'] = df_interact_proc['My_Reaction'].map(REACTION_WEIGHTS)
df_interact_proc['Weighted_Bid_Response'] = df_interact_proc['Vulnerability'] * df_interact_proc['Bid_Weight']
df_interact_proc['P_cycle'] = df_interact_proc['Ps_Weight'] * df_interact_proc['Ur_Weight']

# -------------------------------------------------------------
# 5. UI: Sidebar Navigation (Dating App Removed)
# -------------------------------------------------------------
st.sidebar.title("💾 Data Input Terminal")
log_type = st.sidebar.radio("Select Log Type:", ["🧘 Solo Self-Regulation", "🤝 Active Interaction"])

if log_type == "🧘 Solo Self-Regulation":
    st.sidebar.subheader("New Self-Regulation Entry")
    with st.sidebar.form("self_reg_form", clear_on_submit=True):
        date_sr = st.date_input("Date")
        emotion = st.selectbox("Primary Emotion", ["Secure", "Anxious", "Avoidant", "Lonely", "Overwhelmed", "Resentful", "Peaceful"])
        intensity = st.slider("Intensity (1-10)", 1, 10, 5)
        somatic = st.selectbox("Somatic Location", ["None", "Chest", "Stomach", "Shoulders", "Jaw", "Head"])
        # Dating App removed from triggers
        trigger = st.selectbox("Trigger Event", ["None", "Miscommunication", "Attachment Trigger", "Thought of Ex", "Boundary Crossed", "Loneliness Spike", "Daily Stress"])
        response = st.selectbox("Your Self-Regulation Response", ["Validated", "Suppressed", "Reactive"])
        capacity = st.number_input("Real Free Capacity (Hours)", min_value=0.0, max_value=40.0, value=5.0, step=0.5)
        loneliness_dr = st.slider("Loneliness Level", 1, 10, 5)
        boundary_met = st.selectbox("Did you uphold your boundaries today?", ["Yes", "No", "N/A"])
        
        submit_sr = st.form_submit_button("Record Solo Baseline")
        if submit_sr:
            new_sr = {
                "Date": date_sr.strftime('%Y-%m-%d'), "Emotion": emotion, "Intensity": intensity,
                "Somatic": somatic, "Trigger": trigger, "Response": response,
                "Capacity_Hours": capacity, "Loneliness_Drive": loneliness_dr, "Boundary_Met": boundary_met
            }
            st.session_state.self_reg_df = pd.concat([df_self, pd.DataFrame([new_sr])], ignore_index=True)
            st.rerun()

else:
    st.sidebar.subheader("New Interaction Entry")
    with st.sidebar.form("interaction_form", clear_on_submit=True):
        date_int = st.date_input("Date")
        i_type = st.selectbox("Interaction Type", ["Venting", "Difficult Conversation", "Requesting Closeness", "Casual Check-in"])
        vuln = st.slider("My Vulnerability Level (1-10)", 1, 10, 5)
        
        st.subheader("Gottman Interaction Profiling")
        bid_dir = st.selectbox("Bid Turn Direction", ["Turn Toward (Validating/Responsive)", "Turn Away (Ignoring/Dismissing)", "Turn Against (Critical/Defensive)"])
        horsemen = st.selectbox("Did you detect any of the Four Horsemen?", ["None", "Criticism", "Contempt", "Defensiveness", "Stonewalling"])
        repair = st.selectbox("Did anyone attempt a Repair?", ["No Attempt", "Successful", "Failed"])
        
        st.subheader("Relational Outcomes")
        my_state = st.selectbox("Post-Interaction Feeling", ["Connected", "Lonely/Misunderstood", "Anxious", "Resentful", "Relieved"])
        p_space = st.selectbox("Partner space orientation", ["Approaching", "Neutral", "Withdrawing"])
        my_react = st.selectbox("Your reaction to their withdrawal", ["Regulated & Gave Space", "Pursued Anxiously", "Withdrew in Retaliation", "N/A"])
        
        submit_int = st.form_submit_button("Record Active Interaction")
        if submit_int:
            new_int = {
                "Date": date_int.strftime('%Y-%m-%d'), "Type": i_type, "Vulnerability": vuln,
                "Bid_Direction": bid_dir, "Horsemen": horsemen, "Repair_Attempt": repair,
                "My_State": my_state, "Partner_Space": p_space, "My_Reaction": my_react
            }
            st.session_state.interaction_df = pd.concat([df_interact, pd.DataFrame([new_int])], ignore_index=True)
            st.rerun()

# -------------------------------------------------------------
# 6. Main Dashboard Interface
# -------------------------------------------------------------
st.title("🤝 Advanced Interpersonal Analytics Dashboard")
st.markdown("Detailed mapping of solo self-regulation alongside clinical active relationship dynamics.")
st.markdown("___")

# Master Tabs
tab_solo, tab_relational = st.tabs(["🧘 MODEL 1: Solo Self-Regulation & Readiness", "🤝 MODEL 2: Active Interpersonal Dynamics"])

# -------------------------------------------------------------
# TAB 1: SOLO SELF-REGULATION MODEL
# -------------------------------------------------------------
with tab_solo:
    st.subheader("Personal Baseline, Boundaries, and Capacities")
    
    # Solo Key Stats
    s1, s2, s3 = st.columns(3)
    recent_self = df_self.tail(7)
    
    solo_val_rate = (len(recent_self[recent_self['Response'] == 'Validated']) / len(recent_self)) * 100
    avg_cap = recent_self['Capacity_Hours'].mean()
    boundary_leak = (len(recent_self[recent_self['Boundary_Met'] == 'No']) / len(recent_self)) * 100
    
    s1.metric("Self-Validation Success", f"{solo_val_rate:.0f}%", "Target: >60%")
    s2.metric("Weekly Free Time Budget", f"{avg_cap:.1f} hrs", "Target: >5 hrs")
    s3.metric("Boundary Compromise Rate", f"{boundary_leak:.0f}%", "Target: <20%", delta_color="inverse")
    
    st.markdown("___")
    st.write("### 📊 Solo Model Visualizations (3 Charts)")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # CHART 1: Bandwidth Allocation vs. Loneliness Index
        df_self['Date_parsed'] = pd.to_datetime(df_self['Date'])
        fig_cap_lone = px.line(
            df_self, 
            x='Date_parsed', 
            y=['Capacity_Hours', 'Loneliness_Drive'],
            title="Relational Bandwidth (Capacity) vs. Loneliness Index",
            labels={'value': 'Level', 'variable': 'Metrics'},
            markers=True
        )
        fig_cap_lone.add_hrect(y0=7, y1=10, fillcolor="red", opacity=0.1, line_width=0, annotation_text="Danger Zone: High Loneliness")
        fig_cap_lone.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_cap_lone, use_container_width=True)

    with col_chart2:
        # CHART 2: Somatic Trigger Correlation Map
        df_somatic = df_self[df_self['Somatic'] != 'None']
        if not df_somatic.empty:
            fig_som = px.bar(
                df_somatic, 
                x='Trigger', 
                color='Somatic', 
                title="Somatic Response Map (Mind-Body Connection)",
                labels={'count': 'Occurrences'},
                barmode='group'
            )
            fig_som.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_som, use_container_width=True)
        else:
            st.info("No somatic logs available yet. Check somatic stress indicators in input panel.")

    st.markdown("___")
    col_chart3, col_text = st.columns([1, 1])
    
    with col_chart3:
        # CHART 3: Boundary Maintenance vs. Resentment Triggering
        fig_bound = px.bar(
            df_self, 
            x='Boundary_Met', 
            y='Intensity',
            color='Emotion',
            title="Boundary Protection vs. Emotional Intensity",
            labels={'Boundary_Met': 'Were Boundaries Maintained?', 'Intensity': 'Total Emotional Pressure'},
            barmode='stack'
        )
        fig_bound.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_bound, use_container_width=True)
    
    with col_text:
        st.markdown("### 🧘 Solo Qualitative Analysis")
        avg_lone_sr = recent_self['Loneliness_Drive'].mean()
        if avg_cap < 4.0 and avg_lone_sr > 6.0:
            st.error("**System Diagnostic: Severe Attachment Depletion**")
            st.markdown(
                "You are showing elevated loneliness drives during periods of depleted personal bandwidth. "
                "Seeking deep connectivity in this state typically functions as an escape, leaving you vulnerable "
                "to compromising standard relationship boundaries."
            )
        else:
            st.success("**System Diagnostic: Stable Readiness Baseline**")
            st.markdown(
                "Your capacity, boundary, and emotional validation markers indicate a regulated, balanced state. "
                "You are holding personal boundaries safely and have emotional stability to offer."
            )

# -------------------------------------------------------------
# TAB 2: ACTIVE INTERPERSONAL DYNAMICS (Expanded Model)
# -------------------------------------------------------------
with tab_relational:
    st.subheader("Active Relationship Systems: Attunement, Horsemen, and Conflict Repairs")
    
    # Active Relationship Math Calculations
    recent_int = df_interact_proc.tail(5)
    total_vuln = recent_int['Vulnerability'].sum()
    ev_index = (recent_int['Weighted_Bid_Response'].sum() / total_vuln) if total_vuln > 0 else 0.0
    p_cycle_score = recent_int['P_cycle'].mean()
    
    # Repair success calculations
    total_repairs = len(recent_int[recent_int['Repair_Attempt'] != 'No Attempt'])
    successful_repairs = len(recent_int[recent_int['Repair_Attempt'] == 'Successful'])
    repair_success_rate = (successful_repairs / total_repairs * 100) if total_repairs > 0 else 0.0
    
    # Active Stats Row
    r1, r2, r3 = st.columns(3)
    r1.metric("Bid Turning Efficiency (Ev)", f"{ev_index:+.2f}", "Goal: > +0.5")
    r2.metric("EFT Cycle Polarization (P_cycle)", f"{p_cycle_score:.2f}", "Goal: 0.00 (De-escalated)")
    if total_repairs > 0:
        r3.metric("Repair Success Rate", f"{repair_success_rate:.0f}%", f"{successful_repairs}/{total_repairs} successful")
    else:
        r3.metric("Repair Success Rate", "N/A", "No conflict repairs attempted")
        
    st.markdown("___")
    st.write("### 📊 Active Relationship Visualizations (3 Charts)")
    
    col_chart4, col_chart5 = st.columns(2)
    
    with col_chart4:
        # CHART 4: EFT Cycle Polarization Trendline (Ps * Ur)
        df_interact_proc['Date_parsed'] = pd.to_datetime(df_interact_proc['Date'])
        fig_p_cycle = px.line(
            df_interact_proc, 
            x='Date_parsed', 
            y='P_cycle', 
            title="EFT Pursuit-Withdrawal Polarization History",
            markers=True,
            labels={'P_cycle': 'Polarization Index (Higher = Active Conflict)'}
        )
        fig_p_cycle.add_hline(y=0.0, line_dash="dash", line_color="green", annotation_text="De-escalated / Stable")
        fig_p_cycle.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Active Pursuit-Withdrawal Cycle")
        fig_p_cycle.update_yaxes(range=[-1.2, 1.2])
        fig_p_cycle.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_p_cycle, use_container_width=True)
        st.caption("*Critical Insight:* Tracks the progress of the anxious-avoidant 'Protest Polka' loop. Aim for the line to rest at 0.00.")

    with col_chart5:
        # CHART 5: Vulnerability vs. Bid Turning Response Map
        fig_attune = px.scatter(
            df_interact_proc,
            x="Vulnerability",
            y="Bid_Weight",
            size="Vulnerability",
            color="My_State",
            title="Vulnerability vs. Partner Bid Turning Behavior",
            labels={"Bid_Weight": "Bid Turning Style (R)", "Vulnerability": "My Vulnerability Level (V)"}
        )
        fig_attune.update_yaxes(
            tickmode="array",
            tickvals=[-2, -1, 1],
            ticktext=["Turn Against (-2)", "Turn Away (-1)", "Turn Toward (+1)"]
        )
        fig_attune.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_attune, use_container_width=True)
        st.caption("*Critical Insight:* Maps whether your vulnerability is met with emotional safety (Turning Toward) or rejection (Turning Away/Against).")

    st.markdown("___")
    
    col_chart6, col_diags = st.columns([1, 1])
    
    with col_chart6:
        # CHART 6: Gottman's Four Horsemen & Conflict Repair Efficiency
        # We look at the correlation between the present Horsemen and the success/failure of Repair Attempts
        fig_horse = px.bar(
            df_interact_proc, 
            x="Horsemen", 
            color="Repair_Attempt",
            title="Conflict Horsemen vs. Repair Attempt Success",
            labels={"Horsemen": "Gottman's Four Horsemen Detected", "count": "Occurrences"},
            barmode="group",
            color_discrete_map={"Successful": "#2ca02c", "Failed": "#d62728", "No Attempt": "#7f7f7f"}
        )
        fig_horse.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_horse, use_container_width=True)
        st.caption("*Critical Insight:* If Horsemen (like Stonewalling) are present and Repairs are failing, the conflict is entering high-risk territory.")

    with col_diags:
        st.markdown("### 🗣️ Gottman Conflict & Repair Diagnostic")
        
        # Check for presence of Horsemen (Criticism, Contempt, Defensiveness, Stonewalling)
        recent_horsemen = recent_int[recent_int['Horsemen'] != 'None']
        
        if len(recent_horsemen) >= 2:
            st.error("**Diagnostic Alert: High Risk Conflict Behaviors Detected**")
            st.markdown(
                f"Your recent interactions show frequent activation of **Gottman's Four Horsemen** "
                f"(specifically: *{', '.join(recent_horsemen['Horsemen'].unique())}*). "
                "These behaviors are highly predictive of long-term relational distress and stonewalling."
            )
            st.markdown(
                "**Prescriptive Interventions:**\n"
                "- **Antidote to Criticism:** Use a gentle start-up. Focus on *I-statements* and express a positive need: *'I feel overwhelmed about the house cleanup, could we tackle it together?'* (instead of: *'You never help'*).\n"
                "- **Antidote to Stonewalling:** If physically flooded (heart rate > 100 bpm), call a timeout for at least 20 minutes to calm down before returning to the conversation."
            )
        elif total_repairs > 0 and repair_success_rate < 50.0:
            st.warning("**Diagnostic: Low Repair Efficiency**")
            st.markdown(
                f"You have attempted conflict repairs, but {100 - repair_success_rate:.0f}% of them have failed. "
                "This indicates that the emotional climate is too hot or defensive for repair attempts to take hold."
            )
            st.markdown(
                "**Action Plan:** Ensure you are fully regulated *before* attempting to reconcile. "
                "Instead of debating the issue, offer a physical repair first (e.g., a hug or taking a deep breath together)."
            )
        else:
            st.success("**Diagnostic: Secure Conflict Management**")
            st.markdown(
                "Your conflict repair markers show high resilience. When emotional boundaries or conflicts "
                "occur, you are successfully utilizing repair behaviors to rebuild connection and avoid "
                "damaging defensive spirals."
            )

st.markdown("___")
# Displaying verified raw data structure
with st.expander("📁 View Database Mapping & Active Mathematical Logs"):
    st.write(df_interact_proc[['Date', 'Type', 'Vulnerability', 'Bid_Direction', 'Bid_Weight', 'Horsemen', 'Repair_Attempt', 'My_State', 'Partner_Space', 'My_Reaction', 'P_cycle']])