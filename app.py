import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# CONFIG
st.set_page_config(page_title="AI Smart Home Simulation", layout="wide")
USER_FILE = Path("users.csv")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# USER MANAGEMENT
@st.cache_data(ttl=3600, show_spinner=False)
def load_users_cached():
    if USER_FILE.exists():
        try:
            df = pd.read_csv(USER_FILE, dtype=str).fillna("")
            df["username"] = df["username"].str.strip().str.lower()
            df["password"] = df["password"].str.strip()
            return df
        except Exception as e:
            st.error(f"Error loading users: {e}")
    return pd.DataFrame(columns=["username", "password"])

def save_user(username: str, password: str) -> bool:
    username, password = username.strip().lower(), password.strip()
    df = load_users_cached()
    if username in df["username"].values:
        return False
    new_user = pd.DataFrame([{"username": username, "password": password}])
    pd.concat([df, new_user], ignore_index=True).to_csv(USER_FILE, index=False)
    load_users_cached.clear()
    return True

def validate_user(username: str, password: str) -> bool:
    df = load_users_cached()
    return ((df["username"] == username.strip().lower()) &
            (df["password"] == password.strip())).any()

# SESSION SETUP
def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "devices": {"Light": False, "Fan": False, "AC": False, "TV": False},
        "automation": {"room_auto": True, "temp_threshold_ac": 30},
        "last_log_update": datetime.now() - timedelta(hours=1),
        "room_temp": random.uniform(20, 35)
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

# LOGGING
def get_log_file(username: str) -> Path:
    return LOG_DIR / f"device_log_{username}.csv"

@st.cache_data(ttl=300)
def read_logs_cached(username: str, _n: int = 10):
    log_file = get_log_file(username)
    if log_file.exists():
        df = pd.read_csv(log_file)
        return df.tail(_n).reset_index(drop=True)
    return pd.DataFrame(columns=["Time", "Total Power"])

def save_log(username: str, total_power: float):
    now = datetime.now()
    last_update = st.session_state.get("last_log_update", now - timedelta(hours=1))
    if now - last_update >= timedelta(hours=1):
        log_file = get_log_file(username)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        row = pd.DataFrame([{"Time": timestamp, "Total Power": total_power}])
        if log_file.exists():
            df = pd.read_csv(log_file)
            df = pd.concat([df, row], ignore_index=True)
        else:
            df = row
        df.to_csv(log_file, index=False)
        st.session_state["last_log_update"] = now
        read_logs_cached.clear()
        st.success("Hourly log saved!")

# SIMULATION
def simulate_power_usage(devices):
    return {d: random.randint(50, 300) if s else 0 for d, s in devices.items()}

# AUTOMATION FUNCTION
def apply_room_automation(temp: float):
    auto = st.session_state.automation
    devices = st.session_state.devices
    threshold = auto["temp_threshold_ac"]
    if not auto["room_auto"]:
        return
    if temp >= threshold and not devices["AC"]:
        devices["AC"] = True
        st.success(f"Automation: AC turned ON (Temp: {temp:.1f}°C)")
    elif temp < threshold and devices["AC"]:
        devices["AC"] = False
        st.success(f"Automation: AC turned OFF (Temp: {temp:.1f}°C)")

# COMMAND PARSER
def parse_command(cmd: str):
    cmd = cmd.lower().strip()
    devices = st.session_state.devices
    actions = []
    for device in devices:
        if device.lower() in cmd:
            if "on" in cmd:
                devices[device] = True
                actions.append(f"{device} ON")
            elif "off" in cmd:
                devices[device] = False
                actions.append(f"{device} OFF")
    if "status" in cmd:
        status = ", ".join(f"{k}: {'ON' if v else 'OFF'}" for k, v in devices.items())
        actions.append(f"Status: {status}")
    return actions

# MAIN APP
init_session()

# LOGIN / SIGNUP
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>AI Smart Home Simulation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray'>IoT dashboard with automation</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if validate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username.lower()
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            if st.form_submit_button("Create Account"):
                if new_user and new_pass:
                    if save_user(new_user, new_pass):
                        st.success("Account created! Logging in...")
                        st.session_state.logged_in = True
                        st.session_state.username = new_user.lower()
                        st.rerun()
                    else:
                        st.warning("Username already exists.")
                else:
                    st.error("Please fill all fields.")
    st.stop()

# DASHBOARD
username = st.session_state.get("username", "") or ""
st.markdown(f"<h1 style='text-align:center'>Smart Home Dashboard</h1>", unsafe_allow_html=True)
st.sidebar.title(f"Hi, {username.capitalize() or 'User'}")

# AUTO REFRESH
st_autorefresh(interval=5000, key="refresh_data")

# AUTOMATION SETTINGS
with st.sidebar.expander("Automation", expanded=True):
    st.session_state.automation["room_auto"] = st.checkbox(
        "Temperature Automation",
        value=st.session_state.automation["room_auto"]
    )
    temp_thresh = st.number_input(
        "AC Threshold (°C)",
        min_value=16,
        max_value=45,
        value=int(st.session_state.automation.get("temp_threshold_ac", 30)),
        step=1,
        format="%d",
        help="Temperature (°C) at which the AC will toggle"
    )
    st.session_state.automation["temp_threshold_ac"] = int(temp_thresh)

if st.sidebar.button("Logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# TEMPERATURE SIMULATION (REALISTIC)
change = random.uniform(-0.5, 0.5)
st.session_state.room_temp = max(16, min(40, st.session_state.room_temp + change))
temp = st.session_state.room_temp

# show delta relative to AC threshold (plus if temp > threshold, minus if temp < threshold)
threshold = int(st.session_state.automation.get("temp_threshold_ac", 30))
delta = temp - threshold
st.metric("Room Temp", f"{temp:.1f}°C", delta=f"{delta:+.1f}°C")
st.caption(f"Delta relative to AC Threshold ({threshold}°C)")

# APPLY AUTOMATION
apply_room_automation(temp)

# AUTOMATION STATUS INDICATOR
if st.session_state.automation["room_auto"]:
    st.success(f"Automation ON — AC auto-controls at {st.session_state.automation['temp_threshold_ac']}°C")
else:
    st.warning("Automation OFF — Manual control only")

# DEVICE CONTROLS
st.subheader("Device Control")
cols = st.columns(4)
for i, (device, state) in enumerate(st.session_state.devices.items()):
    # guard column index in case number of devices changes
    col = cols[i % len(cols)]
    with col:
        checked = st.checkbox(device, value=state, key=f"toggle_{device}")
        if checked != state:
            st.session_state.devices[device] = checked

# TEXT CONTROL
st.subheader("Text Control")
cmd_col1, cmd_col2 = st.columns(2)

with cmd_col1:
    st.info("Use the text box to send commands, e.g., 'turn on light' or 'status'.")

with cmd_col2:
    text_cmd = st.text_input("Type command", placeholder="e.g., turn on light", key="text_cmd")
    if text_cmd:
        for a in parse_command(text_cmd):
            if "Status" in a:
                st.info(a)
            else:
                st.success(a)
        st.rerun()

# ENERGY USAGE
st.subheader("Energy Consumption")
usage = simulate_power_usage(st.session_state.devices)
df_usage = pd.DataFrame(list(usage.items()), columns=["Device", "Power (W)"])
total_power = df_usage["Power (W)"].sum()

col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_usage, use_container_width=True)
with col2:
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(df_usage["Device"], df_usage["Power (W)"])
    ax.set_ylim(0, 350)
    ax.set_ylabel("Watts")
    st.pyplot(fig)

st.metric("Total Power", f"{total_power} W")

# LOGS
save_log(username, total_power)
st.subheader("Hourly Logs")
logs = read_logs_cached(username, 8)
if not logs.empty:
    st.dataframe(logs, use_container_width=True)
    next_time = st.session_state.get("last_log_update", datetime.now()) + timedelta(hours=1)
    st.caption(f"Next log: {next_time.strftime('%H:%M:%S')}")
else:
    st.info("No logs yet. First log in about an hour.")

# FOOTER
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>© 2025 Smart Home. All rights reserved.</p>", unsafe_allow_html=True)