from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import uuid

def scan_cookies_for_domain(domain):
    options = Options()

    # HEADLESS + Render-safe config
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    
    # Unikalny katalog dla sesji (usuwa błąd user-data-dir in use)
    tmp_profile = tempfile.mkdtemp(prefix="chrome_profile_" + str(uuid.uuid4())[:8])
    options.add_argument(f"--user-data-dir={tmp_profile}")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        url = f"https://{domain}"
        driver.get(url)

        # Usunięcie preload skryptów cookies-manager
        driver.execute_script("""
            const links = document.querySelectorAll('link[rel="preload"]');
            links.forEach(link => {
                if (link.href.includes('cookies-manager.mr.org.pl')) {
                    link.remove();
                }
            });
        """)

        time.sleep(5)  # daj czas na załadowanie cookies

        cookies = driver.get_cookies()
        cookie_names = [cookie['name'] for cookie in cookies]

        driver.quit()
        return cookie_names

    except WebDriverException as e:
        print(f"Error scanning {domain}: {e}")
        return []
    