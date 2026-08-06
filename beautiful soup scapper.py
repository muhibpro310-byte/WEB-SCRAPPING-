
## url = "https://books.toscrape.com/"

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    )
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    if soup.title:
        print("Page title:", soup.title.get_text(strip=True))
    else:
        print("Page title not found")

    print("\nLinks found:")

    for link in soup.find_all("a"):
        text = link.get_text(" ", strip=True)
        href = link.get("href")

        if href:
            complete_url = urljoin(url, href)

            print(f"{text} -> {complete_url}")

except requests.exceptions.Timeout:
    print("The request timed out.")

except requests.exceptions.ConnectionError:
    print("Could not connect to the website.")

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.RequestException as error:
    print("Request error:", error)