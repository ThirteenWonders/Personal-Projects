import streamlit as st

st.set_page_config(page_title="Phishing Email Analysis", layout="wide")
st.sidebar.title("Phishing Case Explorer")
case = st.sidebar.selectbox("Choose a Page", ["Home", "Case 01", "Case 02", "Case 03"])

def load_case(case):
    if case == "Case 01":
        return {
            "image_url": "https://raw.githubusercontent.com/ThirteenWonders/Personal-Projects/main/Phishing-email-analysis/case01/case1.png",
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
            "image_url": "https://raw.githubusercontent.com/ThirteenWonders/Personal-Projects/main/Phishing-email-analysis/case02/case2.png",
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
            "image_url": "https://raw.githubusercontent.com/ThirteenWonders/Personal-Projects/main/Phishing-email-analysis/case03/case3.png",
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

if case == "Home":
    st.title("📧 Phishing Email Analysis")

    st.markdown("""
    This project documents and analyzes real phishing emails I’ve received (with all personal information censored), highlighting common red flags and social engineering tactics. It is intended to raise awareness and demonstrate practical cybersecurity analysis skills.

    ---

    ## 🧠 Purpose

    Phishing remains one of the most common and effective attack vectors in both personal and enterprise environments. This project aims to:

    - Recognize phishing indicators  
    - Educate others on how to spot phishing attempts  
    - Document real-world examples for awareness and learning  

    ---

    ## 🧩 Structure

    Each phishing email example includes:

    - ✅ **Screenshot** (with personal details censored)  
    - ⚠️ **Red Flags**: A list of suspicious elements identified  
    - 🔍 **Analysis**: Why this email is likely a phishing attempt  
    - 💡 **Takeaway**: What the average user can learn from this case  

    ---

    ## 📂 Examples

    | Case     | Description                                                    | Type                    |
    |----------|----------------------------------------------------------------|-------------------------|
    | Case 01  | Fake Microsoft Office365 renewal failure notice                | Credential Harvesting   |
    | Case 02  | Fake Gemini login alert with suspicious attachment             | Tech Support Scam       |
    | Case 03  | Fake Gemini-to-Exodus wallet migration requesting seed phrase  | Cryptocurrency Phishing |

    ---

    ## 📝 Case Highlight

    **⚠️ Case 03 stands out as a highly deceptive phishing attempt.**  
    It closely mimics a legitimate email from Gemini, referencing real-world topics such as SEC regulatory compliance and self-custody. The message includes:

    - **Authentic-looking branding and layout**  
    - **Use of actual Gemini contact addresses** like `support@gemini.com` and `security@gemini.com`  
    - A **realistic narrative** around crypto migration to Exodus wallets  
    - A fake but convincingly formatted **12-word seed phrase**, which if used, would directly compromise a user's crypto assets

    > This example illustrates how phishing emails are evolving to appear nearly indistinguishable from legitimate communications — making awareness and analysis more important than ever.

    ---

    ## 🚫 Safety Disclaimer

    - All screenshots are sanitized and do **not** contain any clickable or live malicious links.
    - Any URLs are obfuscated (e.g., `hxxp://`) to prevent accidental access.

    ---

    ## 🙋 Who Is This For?

    - Anyone wanting to improve their phishing detection awareness

    ---

    ## 📌 Note

    This is a personal project for learning and awareness. If you'd like to suggest improvements, corrections, or ideas, feel free to open an issue or contribute via pull request.

    ---
    """)

else:
    data = load_case(case)
    st.title(case)
    st.image(data["image_url"], caption="Phishing Email Screenshot", use_container_width=True)

    st.subheader("⚠️ Red Flags")
    for flag in data["red_flags"]:
        st.markdown(f"- {flag}")

    st.subheader("🔍 Analysis")
    st.write(data["analysis"])

    st.subheader("✅ Recommendations")
    for rec in data["recommendations"]:
        st.markdown(f"- {rec}")

    if case == "Case 03":
        st.warning("⭐ This is a particularly deceptive phishing attempt that mimics real Gemini branding and includes actual company support addresses. Always verify claims through official sources.")
