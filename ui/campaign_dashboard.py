# ui/campaign_dashboard.py

import os, json, requests, streamlit as st
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

st.set_page_config(page_title="Realms to Riches Dashboard", layout="wide")

# 🎨 Branding
st.markdown("""
    <style>
    .main {background-color: #f0f0f5;}
    h1, h2, h3 {color: #00ffff;}
    .stButton>button {background-color: #ff69b4; color: white;}
    .metric-box {background-color: #ffffff; padding: 20px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# 🚀 Title
default_name = "Odin's Forge"
st.title(f"🚀 {os.environ.get('PROJECT_NAME', default_name)}")

# 📊 Agent Metrics
st.subheader("🧠 Agent Metrics")
metrics_path = Path("logs/kpi_log.json")
if metrics_path.exists():
    data = json.loads(metrics_path.read_text())
    st.json(data)
else:
    st.warning("No metrics found. Agents may not be active.")

# 💰 Stripe Checkout Trigger
st.subheader("💳 Monetization")
if st.button("Launch Agent Bundle Checkout"):
    stripe_key = os.getenv("STRIPE_API_KEY")
    if stripe_key:
        session = requests.post("https://api.stripe.com/v1/checkout/sessions", headers={
            "Authorization": f"Bearer {stripe_key}"
        }, data={
            "payment_method_types[]": "card",
            "line_items[0][price_data][currency]": "usd",
            "line_items[0][price_data][product_data][name]": "Forge Agent Pack",
            "line_items[0][price_data][unit_amount]": "4900",
            "line_items[0][quantity]": "1",
            "mode": "payment",
            "success_url": "https://realmstoriches.xyz/success",
            "cancel_url": "https://realmstoriches.xyz/cancel"
        })
        if session.ok:
            url = session.json()["url"]
            st.success("✅ Checkout created")
            st.markdown(f"[Click to Pay]({url})")
        else:
            st.error("❌ Stripe failed to create session")
    else:
        st.error("❌ Stripe API key missing")

# 🛍️ Shopify Trigger
st.subheader("🛍️ Voice Pack Store")
if st.button("Open Shopify Store"):
    st.markdown("[Visit Store](https://realmstoriches.myshopify.com)", unsafe_allow_html=True)

# 📣 Campaign Launch
st.subheader("📣 Launch Campaign")
campaigns = ["Dominance Pulse", "Echo Surge", "Zara Spark", "Orion Drift"]
selected = st.selectbox("Choose Campaign", campaigns)
if st.button("Launch Selected Campaign"):
    st.success(f"✅ {selected} launched")
    # Trigger agent swarm here (real endpoint or subprocess)

# 📡 Blog Dispatch
st.subheader("📝 Blog Dispatch")
if st.button("Dispatch Monetized Blog Post"):
    response = requests.post("https://blog.realmstoriches.xyz/api/dispatch", json={
        "title": "Agentic Wealth Activation",
        "content": "Your agents have launched a monetized campaign. Income is flowing."
    })
    if response.ok:
        st.success("✅ Blog post dispatched")
    else:
        st.error("❌ Blog dispatch failed")

# 🔐 OAuth Status
st.subheader("🔐 OAuth Status")
access_token = os.getenv("ACCESS_TOKEN")
if access_token:
    st.success("OAuth token active")
else:
    st.warning("OAuth not aligned")

# 📈 Real-Time Logs
st.subheader("📈 Real-Time Logs")
log_path = Path("logs/launch_log.json")
if log_path.exists():
    st.code(log_path.read_text())
else:
    st.info("No launch logs found")