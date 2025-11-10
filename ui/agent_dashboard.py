import streamlit as st
import json
from pathlib import Path
from datetime import datetime

LOGS = Path("logs")
st.set_page_config(page_title="Agent Dashboard", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0f0f0f;
        color: #f5f5f5;
    }
    h1, h2, h3 {
        color: #00FFFF;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #1a1a1a;
    }
    .stSidebar {
        background-color: #111111;
    }
    .stMarkdown {
        font-family: 'Courier New', monospace;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)


st.title("🧠 Realms to Riches — Agent Activity Monitor")

def load_log(file):
    path = LOGS / file
    if not path.exists():
        return []
    try:
        content = path.read_text()
        # If multiple JSON blobs exist, extract the first valid array
        if content.strip().startswith("["):
            return json.loads(content)
        else:
            # Attempt to isolate the first array
            start = content.find("[")
            end = content.find("]", start) + 1
            return json.loads(content[start:end])
    except json.JSONDecodeError as e:
        st.error(f"⚠️ Failed to load {file}: {e}")
        return []

# ─── Sidebar Filters ─────────────────────────────────────
st.sidebar.header("Filters")
selected_agent = st.sidebar.selectbox("Agent", ["All"] + [
    entry["agent"] for entry in load_log("dispatch_log.json")
])
cycle_limit = st.sidebar.slider("Max Cycles", 1, 20, 7)

# ─── Dispatch Log ────────────────────────────────────────
st.subheader("⚡ Dispatch Activity")
dispatches = load_log("dispatch_log.json")
if selected_agent != "All":
    dispatches = [d for d in dispatches if d["agent"] == selected_agent]
for entry in dispatches[-cycle_limit:]:
    st.markdown(f"""
- **Agent:** {entry['agent']}
- **Role:** {entry['role']}
- **Campaign:** {entry['campaign']}
- **Dispatch Confirmed:** ✅
- **Channel Connected:** {'✅' if entry.get('channel_connected') else '❌'}
- **Time:** {entry['timestamp']}
""")

# ─── KPI Log ─────────────────────────────────────────────
st.subheader("📊 Agent KPIs")
kpis = load_log("kpi_log.json")
if selected_agent != "All":
    kpis = [k for k in kpis if k["agent"] == selected_agent]
for entry in kpis[-cycle_limit:]:
    st.markdown(f"""
- **Agent:** {entry['agent']}
- **Tasks Completed:** {entry['tasks_completed']}
- **Fallback Used:** {'✅' if entry['fallback_used'] else '❌'}
- **Confidence Score:** {entry['confidence']}
- **Time:** {entry['timestamp']}
""")

# ─── Messaging Log ───────────────────────────────────────
st.subheader("💬 Agent Messaging")
messages = load_log("agent_messages.json")
if selected_agent != "All":
    messages = [m for m in messages if m["from"] == selected_agent or m["to"] == selected_agent]
for entry in messages[-cycle_limit:]:
    st.markdown(f"""
- **From:** {entry['from']}
- **To:** {entry['to']}
- **Message:** {entry['message']}
- **Time:** {entry['timestamp']}
""")

# ─── UI Patch Log ────────────────────────────────────────
st.subheader("🧩 UI Agent Patching")
patches = load_log("ui_patch_log.json")
if selected_agent != "All":
    patches = [p for p in patches if p["agent"] == selected_agent]
for entry in patches[-cycle_limit:]:
    st.markdown(f"""
- **Agent:** {entry['agent']}
- **Action:** {entry['action']}
- **Time:** {entry['timestamp']}
""")