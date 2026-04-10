import streamlit as st
import json
import os
from agent_system import monitoring_agent, analysis_agent, response_agent, explanation_agent
if "history" not in st.session_state:
    st.session_state.history = []
st.set_page_config(page_title="Cyber AI Agent", layout="centered")

st.title("🛡️ Multi-Agent Cyber Threat Intelligence & Response System")

# ---------------- INPUT ----------------
input_type = st.selectbox("Select Input Type", ["IP", "URL", "HASH"])
user_input = st.text_input("Enter value")

# ---------------- ANALYZE ----------------
if st.button("Analyze"):

    if not user_input:
        st.warning("Please enter a value")
    else:
        with st.spinner("Analyzing... 🔍"):

            data = monitoring_agent(user_input)
            result = analysis_agent(data, input_type)

            response_agent(result)

        # ---------------- STATUS UI ----------------
        if result.get("status") == "THREAT":
            st.error("🚨 Threat Detected!")
        elif result.get("status") == "SAFE":
            st.success("✅ Safe")
        else:
            st.info("ℹ️ Processed")

        # ---------------- RESULT ----------------
        st.write("## 🔍 Result")
        st.json(result)

        # ---------------- GEO INFO ----------------
        if input_type == "IP":
            st.write("🌍 Location:")
            st.write("Country:", result.get("country"))
            st.write("City:", result.get("city"))

        # ---------------- AI EXPLANATION ----------------
        st.write("### 🧠 AI Explanation")
        st.write(explanation_agent(result))

        # ---------------- DOWNLOAD REPORT ----------------
        st.download_button(
            "📄 Download Report",
            data=json.dumps(result, indent=4),
            file_name="report.json",
            mime="application/json"
        )

        # ---------------- SAVE HISTORY ----------------
        with open("history.json", "a") as f:
            f.write(json.dumps(result) + "\n")


# ---------------- HISTORY BUTTON ----------------
# ---------------- HISTORY SEARCH ----------------

# ✅ Step 1: Store button state
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Button click
if st.button("📊 Show History"):
    st.session_state.show_history = True

# ✅ Step 2: Keep UI visible
if st.session_state.show_history:

    st.write("## 🔍 Search History")

    search_ip = st.text_input("Enter IP to view history", key="history_input")

    if search_ip:
        if os.path.exists("history.json"):
            with open("history.json") as f:
                lines = f.readlines()

                found = False

                for line in lines:
                    data = json.loads(line)

                    if data.get("input") == search_ip:
                        st.json(data)
                        found = True

                if not found:
                    st.info("No history found for this IP")
        else:
            st.info("No history file found")