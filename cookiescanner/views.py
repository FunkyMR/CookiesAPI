from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CookieData
from .serializers import CookieDataSerializer

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

VALID_API_KEYS = ['abc123']

class CookieScanView(APIView):
    def post(self, request):
        api_key = request.data.get("api_key")
        domains = request.data.get("domains")

        if api_key not in VALID_API_KEYS:
            return Response({"error": "Invalid API key."}, status=403)

        if not isinstance(domains, list):
            return Response({"error": "Expected 'domains' as list."}, status=400)

        results = {}

        for domain in domains:
            cookie_names = self.scan_cookies(domain)
            if cookie_names is None:
                continue

            CookieData.objects.update_or_create(
                domain=domain,
                defaults={
                    "cookies": cookie_names,
                    "updateDate": timezone.now()
                }
            )
            results[domain] = cookie_names

        return Response(results, status=200)

    def scan_cookies(self, domain):
        options = Options()
        # options.headless = True
        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        try:
            driver = webdriver.Chrome(options=options)
            driver.get(f"http://{domain}")

            # Usunięcie preload skryptów cookies-manager
            driver.execute_script("""
                const links = document.querySelectorAll('link[rel="preload"]');
                links.forEach(link => {
                    if (link.href.includes('cookies-manager.mr.org.pl')) {
                        link.remove();
                    }
                });
            """)

            time.sleep(5)  # Dajemy stronie czas na załadowanie cookies

            cookies = driver.get_cookies()
            cookie_names = [cookie['name'] for cookie in cookies]

            driver.quit()
            return cookie_names
        except Exception as e:
            print(f"Błąd przy {domain}: {e}")
            return None
