import streamlit as st
from PIL import Image

# Title and Sidebar
st.set_page_config(page_title="Phishing Email Analysis", layout="wide")
st.sidebar.title("Phishing Case Explorer")
case = st.sidebar.selectbox("Choose a Case", ["Case 01", "Case 02", "Case 03"])

# Case Data
def load_case(case):
    if case == "Case 01":
        return {
            "image_path": "Phishing email analysis/Case 01/Case1.png",
            "red_flags": [
                "Sender domain is not Microsoft: refreshfaces.com",
                "Suspicious .mobileconfig attachment",
                "Low-quality Microsoft logo",
                "Urgent call to action to update billing info",
                "Unrelated content (Postnup and Will)",
            ],
            "analysis": "This email impersonates Microsoft and urges the recipient to update billing information. It includes a suspicious file attachment and has inconsistencies in language and layout.",
            "recommendations": [
                "Do not open attachments from unknown senders",
                "Verify email sender domains",
                "Report phishing emails to your IT department"
            ]
        }
    elif case == "Case 02":
        return {
            "image_path": "Phishing email analysis/Case 02/Case2.png",
            "red_flags": [
                "Sender domain not associated with Gemini",
                "Includes .mobileconfig attachment",
                "Scare tactic: unauthorized login from unknown device",
                "Fake support number instead of a link to the official site",
                "Lack of personal greeting or account detail reference"
            ],
            "analysis": "This phishing email attempts to create panic by reporting a suspicious login. The goal is to make the recipient call a scam support number or install a malicious attachment.",
            "recommendations": [
                "Do not trust phone numbers from unsolicited emails",
                "Never open .mobileconfig files unless verified",
                "Always check login alerts directly through official apps or sites"
            ]
        }
    elif case == "Case 03":
        return {
            "image_path": "Phishing email analysis/Case 03/Case3.png",
            "red_flags": [
                "Sender domain is spoofed (not gemini.com)",
                "References real-world regulation for believability",
                "Fake seed phrase provided directly in the email",
                "Urgent transfer timeline adds pressure",
                "High-quality formatting mimics a real Gemini email"
            ],
            "analysis": "This email is highly deceptive. It uses real-world regulatory context (SEC) and professional design to trick users into importing a fake seed phrase, which would compromise their wallet.",
            "recommendations": [
                "Never share or enter your wallet seed phrase",
                "Verify migration notices on the official Gemini site",
                "Be extra cautious with crypto-related emails"
            ]
        }

# Load content
data = load_case(case)

# Display Content
st.title(case)

# Image
try:
    st.image(Image.open(data["image_path"]), caption="Phishing Email Screenshot", use_column_width=True)
except FileNotFoundError:
    st.error("Image not found. Please ensure the file path is correct.")

# Red Flags
st.subheader("⚠️ Red Flags")
for flag in data["red_flags"]:
    st.markdown(f"- {flag}")

# Analysis
st.subheader("🔍 Analysis")
st.write(data["analysis"])

# Recommendations
st.subheader("✅ Recommendations")
for rec in data["recommendations"]:
    st.markdown(f"- {rec}")

# Highlight for Case 03
if case == "Case 03":
    st.warning("⭐ This is a particularly deceptive phishing attempt that mimics real Gemini branding and includes actual company support addresses. Always verify claims through official sources.")
