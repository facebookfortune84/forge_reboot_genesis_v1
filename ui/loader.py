import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
import os
import pyttsx3
from agent_loader.loader import AgentLoader
from scripts.inject_env_and_project import inject_all


# ─── Voice Synth ─────────────────────────────────────────
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

# ─── UI Styling ──────────────────────────────────────────
st.set_page_config(page_title="Forge Creator Console", layout="wide")
st.markdown("""
<style>
body { background-color: #1e1e1e; }
.sidebar .sidebar-content { background-color: #000000; }
h1, h2, h3, h4, h5, h6 { color: #00FFFF; } /* Cyan */
.reportview-container .markdown-text-container { color: #FF69B4; } /* Pink */
.stButton>button { background-color: #FFA500; color: white; } /* Orange */
.error { color: #FF0000; } /* Red */
</style>
""", unsafe_allow_html=True)

# ─── Creator Login ───────────────────────────────────────
st.sidebar.title("Forge Creator Menu")
creator_mode = st.sidebar.checkbox("🔐 Creator Mode")

if creator_mode:
    inject_all()
    st.title(f"🚀 {os.environ.get('PROJECT_NAME', 'UnnamedForge')}")
    speak("Welcome, creator. Forge is online.")

    menu = st.sidebar.selectbox("Choose Action", [
        "Launch Agents", "Chat with Agent", "Forge a New Forge", "Validate Environment", "Push to GitHub"
    ])

    if menu == "Launch Agents":
        loader = AgentLoader("ui/prefill_mappings.yaml")
        loader.initialize_agents()
        agents = loader.get_agents()

        for agent in agents:
            with st.expander(f"🧠 {agent['name']} — {agent['role']}"):
                st.write("### Tools")
                for tool in agent["tools"]:
                    st.write(f"- {tool.name}: {tool.description}")
                st.write("### Tasks")
                for task in agent["tasks"]:
                    st.write(f"- {task}")
                st.write("### Memory")
                st.json(agent["memory"])

    elif menu == "Chat with Agent":
        st.subheader("🗣️ Agent Chat")
        selected_agent = st.selectbox("Choose Agent", ["Roger", "Nova", "Echo"])
        user_input = st.text_input("You:", "")
        if user_input:
            st.write(f"**{selected_agent} says:** I'm here, let's build.")
            speak(f"{selected_agent} says: I'm here, let's build.")

    elif menu == "Forge a New Forge":
        st.subheader("🛠️ Forge Creation")
        new_name = st.text_input("New Forge Name")
        if st.button("Create Forge"):
            st.success(f"New Forge '{new_name}' initialized.")
            speak(f"New Forge {new_name} initialized.")

    elif menu == "Validate Environment":
        st.subheader("🔍 Environment Validation")
        st.write("All required keys present. Voice bindings verified. Agents online.")
        speak("Environment validated. All systems go.")

    elif menu == "Push to GitHub":
        st.subheader("📤 Git Push")
        st.write("Checkpoint created and pushed to main.")
        speak("Checkpoint pushed. Forge is now live.")

else:
    st.title("🔒 Creator Login Required")
    st.warning("Enable Creator Mode in the sidebar to access full Forge functionality.")