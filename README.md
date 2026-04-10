**🛡️ Multi-Agent Cyber Threat Intelligence & Response System**

**1. 🔍 Business Problem**
Cyber attacks are increasing. They include malicious IP addresses, URLs, and file hashes which can be detected and mitigated through external APIs.

**2. 💡 Possible Solution**
A system capable of:
Input analysis (IP/URL/HASH)
Threat detection via external APIs
Sending alerts and running workflows
Log generation for future analytics

**3. 🚀 Implemented Solution**
Developing a Multi-agent Cyber Threat Intelligence system with:
Multiple agents (Monitors, Analyzers, Responders, Explainers)
Analysis of threats via abuseipdb and VirusTotal
Automation using n8n
Logging in Google sheets
Web interface for analysis and searches

**4. 🛠️ Tech Stack Used**
Python (backend logic)
Streamlit (frontend UI)
n8n (workflow automation)
AbuseIPDB API (IP analyzer)
VirusTotal API (URL/Hash analyzer)
Google Sheets (database for logging)

**5. 🧩 Architecture Diagram**

👉 (add the diagram to the README)

User Input (Website)
            ↓
Monitor agent
            ↓
Analyzer Agent (via APIs)
            ↓
Decision (THREAT/SAFE)
            ↓
Responder agent
            ↓
Automation (n8n)
            ↓
Google Sheets (with email alerts)
 

**6. ▶️ How to Run Locally**
# Step 1
pip install requests streamlit python-dotenv

# Step 2
.env file
ABUSE_API_KEY=your_api_key
VT_API_KEY=your_api_key

# Step 3
Run n8n
n8n start

# Step 4
run app
python -m streamlit app.py


**7. 📚 References & Resources**
https://www.abuseipdb.com/
https://www.virustotal.com/
https://docs.n8n.io/
https://docs.streamlit.io/

**8. Recording **

**9. 📸 Screenshot**

Website UI 

n8n workflow 
 
Output from Google Sheets
 

**10. 📐 Formatting**

✔ Headings used
✔ Bullet points used
✔ Spacing is clean

**11. ⚠️ Problems Encountered and Solutions**
During the development of this project, several challenges were encountered. One of the main issues was handling API errors, as external APIs like AbuseIPDB and VirusTotal sometimes returned unexpected responses or failed requests. This was resolved by implementing proper error handling using try-except blocks to ensure the system remained stable. Another challenge was the Streamlit rerender issue, where UI elements such as buttons and inputs would reset on every interaction. This was addressed by using session_state to maintain state across reruns. Additionally, there was a problem with data not mapping correctly in n8n, as the system initially returned unstructured text instead of JSON. This was fixed by restructuring the output into proper JSON format for seamless integration. Lastly, the history feature initially disappeared due to temporary storage in memory; this was solved by implementing persistent storage using a local JSON file, allowing retrieval and filtering of past records efficiently.
