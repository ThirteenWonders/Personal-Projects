
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebSecurityScanner:
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.visited_urls = set()
        self.vulnerabilities = []
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            '\"<img src=x onerror=alert(\'XSS\')>',
            "<svg onload=alert('XSS')>"]

    def login(self):
        login_url = urllib.parse.urljoin(self.target_url, "login.php")
        response = self.session.get(login_url)
        soup = BeautifulSoup(response.text, "html.parser")
        token = soup.find("input", {"name": "user_token"})
        token_value = token['value'] if token else ''

        payload = {
            "username": "admin",
            "password": "password",
            "user_token": token_value,
            "Login": "Login"
        }

        post_login = self.session.post(login_url, data=payload, headers=self.headers)
        if "logout.php" in post_login.text:
            print("[+] Logged in successfully.")
        else:
            print("[-] Login failed.")

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urllib.parse.urljoin(url, link["href"])
                if self.target_url in full_url:
                    self.crawl(full_url)
        except:
            pass

    def report_vulnerability(self, vuln_type, url, parameter, payload):
        info = {
            "type": vuln_type,
            "url": url,
            "parameter": parameter,
            "payload": payload
        }
        self.vulnerabilities.append(info)
        print("[VULNERABILITY FOUND]")
        for k, v in info.items():
            print(f"{k}: {v}")
        print()

    def detect_sensitive_info(self, url):
        try:
            response = self.session.get(url)
            patterns = [r"password.*=", r"token", r"secret"]
            for pattern in patterns:
                match = re.search(pattern, response.text, re.IGNORECASE)
                if match:
                    self.report_vulnerability("Sensitive Information Exposure", url, "match", match.group(0))
        except:
            pass

    def detect_get_sql_injection(self, url):
        sql_payloads = ["'", "1' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--"]
        parsed = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed.query)

        for param in query_params:
            for payload in sql_payloads:
                test_query = query_params.copy()
                test_query[param] = [payload]

                new_query = urllib.parse.urlencode(test_query, doseq=True)
                new_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                                                   parsed.params, new_query, parsed.fragment))
                try:
                    response = self.session.get(new_url)
                    if any(err in response.text.lower() for err in ['sql', 'mysql', 'syntax']):
                        self.report_vulnerability("SQL Injection (GET-based)", new_url, param, payload)
                except:
                    continue

    def detect_xss(self, url):
        print("[*] Launching browser to test for reflected XSS...")
        for payload in self.xss_payloads:
            parsed = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed.query)

            for param in query_params:
                test_query = query_params.copy()
                test_query[param] = [payload]
                test_url = urllib.parse.urlunparse(
                    parsed._replace(query=urllib.parse.urlencode(test_query, doseq=True)))

                try:
                    chrome_options = Options()
                    chrome_options.add_argument("--headless=new")
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                    driver.get(test_url)

                    try:
                        # Wait up to 5 seconds for alert to appear
                        WebDriverWait(driver, 5).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.dismiss()
                        self.report_vulnerability("Reflected XSS", test_url, param, payload)
                    except:
                        pass  # No alert = no XSS triggered

                    driver.quit()

                except Exception as e:
                    print(f"XSS test failed on {test_url}: {e}")

    def run(self):
        self.login()
        self.crawl()
        for url in self.visited_urls:
            self.detect_get_sql_injection(url)
            self.detect_sensitive_info(url)
            self.detect_xss(url)

        print(f"URLs scanned: {len(self.visited_urls)}")
        print(f"Vulnerabilities detected: {len(self.vulnerabilities)}")
        print("Summary of Vulnerabilities by Type:")
        counts = Counter(v['type'] for v in self.vulnerabilities)
        for vtype, count in counts.items():
            print(f"  {vtype}: {count}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scanner_final.py <target_url>")
    else:
        scanner = WebSecurityScanner(sys.argv[1])
        scanner.run()
