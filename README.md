# Web Vulnerability Scanner

This project is a Python-based **Web vulnerability scanner** designed for educational and testing purposes against deliberately insecure web applications like **Damn Vulnerable Web Application (DVWA)**. It automates detection of common web vulnerabilities using both HTTP requests and browser automation via Selenium.

## 🔍 Features

- ✅ **Login automation** (supports CSRF tokens)
- ✅ **Recursive crawling** of the target website
- ✅ **Detection of**:
  - ✅**Sensitive Information Exposure**
  - ✅**SQL Injection (GET-based)**
  - **Reflected Cross-Site Scripting (XSS)** (via Selenium browser automation) *Still work in progress

## 📦 Technologies Used

- `requests` – for HTTP session management  
- `BeautifulSoup` – for HTML parsing  
- `re` – for pattern matching  
- `Selenium` – for dynamic XSS testing in a browser  
- `ChromeDriver` – controlled using `webdriver-manager`

## 🚀 How to Run

1. Ensure DVWA is running locally at: `http://localhost:8080`
2. Set DVWA **security level to "Low"**
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Docker
Docker was used to run the DVWA environment in a container
<br/>
WARNING: DO NOT DEPLOY DVWA IN A INTERNET FACING HOST
