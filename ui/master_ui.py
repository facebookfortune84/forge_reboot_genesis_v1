import streamlit as st
# [FIXED] import yaml
# [FIXED] import os
from agent_loader.yaml_tool_injector import inject_tools_into_yaml
from agent_loader.loader import AgentLoader
from inject_env_and_project import inject_all

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def launch_master_ui():
    inject_all()
    st.set_page_config(page_title="Forge Builder", layout="wide")
    st.title("🧪 Forge Builder Control Panel")

    mappings = load_yaml("ui/prefill_mappings.yaml")
    agents = mappings.get("agents", [])

    st.sidebar.header("🔧 Tool Injection")
    tool_list = st.sidebar.multiselect("Select tools to inject", [
        "FacebookTool", "LinkedInTool", "ShopifyTool",
        "VoiceTool", "WordPressTool", "StripeTool"
    ])
    if st.sidebar.button("Inject Tools"):
        inject_tools_into_yaml("ui/prefill_mappings.yaml", tool_list)
        st.sidebar.success("Tools injected.")

    st.sidebar.header("🚀 Launch Forge")
    if st.sidebar.button("Launch Inner UI"):
        st.sidebar.markdown("Run: `streamlit run ui/launch_ui.py`")

    st.write("### Agent Preview")
    loader = AgentLoader("ui/prefill_mappings.yaml")
    loader.initialize_agents()
    for agent in loader.get_agents():
        st.subheader(agent["name"])
        st.write(f"**Role:** {agent['role']}")
        st.write(f"**Tools:** {[t.name for t in agent['tools']]}")
        st.write(f"**Tasks:** {agent['tasks']}")
        st.json(agent["memory"])

if __name__ == "__main__":
    launch_master_ui()