import requests
import os
import re
import datetime
from dotenv import load_dotenv

load_dotenv()

ABUSE_API_KEY = os.getenv("ABUSE_API_KEY")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY")


# -------------------------------
# Monitoring Agent
# -------------------------------
def monitoring_agent(input_data):
    return input_data


# -------------------------------
# Guardrail (IP validation)
# -------------------------------
def is_valid_ip(ip):
    return re.match(r"\d+\.\d+\.\d+\.\d+", ip)


# -------------------------------
# 🌍 GEOLOCATION FUNCTION
# -------------------------------
def get_ip_location(ip):
    try:
        # 1️⃣ Try ipinfo (with API key)
        url = f"https://ipinfo.io/{ip}?token={IPINFO_API_KEY}"
        res = requests.get(url)
        data = res.json()

        if data.get("country"):
            return {
                "country": data.get("country"),
                "city": data.get("city", "Unknown")
            }

        # 2️⃣ Fallback to free API (no key)
        fallback = requests.get(f"http://ip-api.com/json/{ip}").json()

        return {
            "country": fallback.get("country", "Unknown"),
            "city": fallback.get("city", "Unknown")
        }

    except Exception as e:
        print("Geo Error:", e)
        return {
            "country": "Unknown",
            "city": "Unknown"
        }


# -------------------------------
# Analysis Agent (Multi Input)
# -------------------------------
def analysis_agent(input_value, input_type="IP"):

    result = {
        "input": input_value,
        "type": input_type,
        "time": str(datetime.datetime.now())
    }

    try:
        # ---------------- IP CHECK ----------------
        if input_type == "IP":

            if not is_valid_ip(input_value):
                return {"error": "Invalid IP address"}

            url = "https://api.abuseipdb.com/api/v2/check"
            headers = {
                "Key": ABUSE_API_KEY,
                "Accept": "application/json"
            }
            params = {
                "ipAddress": input_value,
                "maxAgeInDays": 90
            }

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            score = data["data"]["abuseConfidenceScore"]
            status = "THREAT" if score > 50 else "SAFE"

            location = get_ip_location(input_value)

            result.update({
                "score": score,
                "status": status,
                "country": location["country"],
                "city": location["city"]
            })

        # ---------------- URL CHECK ----------------
        elif input_type == "URL":
            url = "https://www.virustotal.com/api/v3/urls"
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}

            requests.post(url, headers=headers, data={"url": input_value})

            result.update({
                "status": "CHECKED",
                "note": "URL submitted to VirusTotal"
            })

        # ---------------- HASH CHECK ----------------
        elif input_type == "HASH":
            url = f"https://www.virustotal.com/api/v3/files/{input_value}"
            headers = {"x-apikey": VIRUSTOTAL_API_KEY}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                result.update({
                    "status": "THREAT",
                    "note": "File flagged by VirusTotal"
                })
            else:
                result.update({
                    "status": "SAFE",
                    "note": "No record found"
                })

    except Exception as e:
        result["error"] = str(e)

    return result


# -------------------------------
# Response Agent (n8n webhook)
# -------------------------------
def response_agent(result):
    try:
        requests.post(
            "https://mitered-nongilded-brittani.ngrok-free.dev/webhook-test/alert",
            json=result
        )
    except:
        pass


# -------------------------------
# AI Explanation Agent
# -------------------------------
def explanation_agent(result):
    if result.get("status") == "THREAT":
        return "🚨 This input shows suspicious activity and high risk."
    elif result.get("status") == "SAFE":
        return "✅ This input appears safe with no major threats."
    else:
        return "ℹ️ Input processed successfully."