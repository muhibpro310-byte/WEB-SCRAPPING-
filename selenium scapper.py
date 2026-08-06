from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# ---------------------------------------------------------
# WEBSITE SETTINGS
# ---------------------------------------------------------

URL = "https://quotes.toscrape.com/js/"
# CSV file will be created beside this Python file.
OUTPUT_FILE = Path(__file__).resolve().with_name("quotes_data.csv")


# ---------------------------------------------------------
# CHROME SETTINGS
# ---------------------------------------------------------
options = webdriver.ChromeOptions()
# Open Chrome in a maximized window.
options.add_argument("--start-maximized")

# Disable browser notifications.
options.add_argument("--disable-notifications")

# Reduce unnecessary browser messages.
options.add_experimental_option(
    "excludeSwitches",
    ["enable-logging"]
)

# Selenium automatically manages ChromeDriver.
driver = webdriver.Chrome(options=options)

# Wait up to 15 seconds for website elements.
wait = WebDriverWait(driver, 15)


# ---------------------------------------------------------
# STORAGE FOR SCRAPED DATA
# ---------------------------------------------------------

all_quotes = []


try:
    # -----------------------------------------------------
    # OPEN THE WEBSITE
    # -----------------------------------------------------

    print("Opening website...")

    if not URL.startswith(("http://", "https://")):
        raise ValueError(
            "The URL must start with http:// or https://"
        )

    driver.get(URL)

    print("Website opened successfully.")
    print("Page title:", driver.title)


    # -----------------------------------------------------
    # SCRAPE ALL PAGES
    # -----------------------------------------------------

    page_number = 1

    while True:
        print(f"\nScraping page {page_number}...")

        # Wait until JavaScript loads the quote cards.
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.quote")
            )
        )

        # Get the fully rendered HTML from Selenium.
        html = driver.page_source

        # Pass the HTML to BeautifulSoup.
        soup = BeautifulSoup(html, "html.parser")

        # Find all quote cards.
        quote_cards = soup.select("div.quote")

        print(f"Quotes found on page: {len(quote_cards)}")


        # -------------------------------------------------
        # EXTRACT DATA FROM EVERY QUOTE CARD
        # -------------------------------------------------

        for card in quote_cards:

            quote_element = card.select_one("span.text")
            author_element = card.select_one("small.author")
            tag_elements = card.select("a.tag")

            quote_text = (
                quote_element.get_text(strip=True)
                if quote_element
                else "Not available"
            )

            author = (
                author_element.get_text(strip=True)
                if author_element
                else "Not available"
            )

            tags = [
                tag.get_text(strip=True)
                for tag in tag_elements
            ]

            tags_text = ", ".join(tags)

            record = {
                "Quote": quote_text,
                "Author": author,
                "Tags": tags_text,
                "Page": page_number
            }

            all_quotes.append(record)

            print(f"Extracted: {author}")


        # -------------------------------------------------
        # FIND AND CLICK THE NEXT BUTTON
        # -------------------------------------------------

        next_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "li.next a"
        )

        # Stop when the Next button no longer exists.
        if not next_buttons:
            print("\nNo Next button found.")
            print("All pages have been scraped.")
            break

        # Store the first quote so Selenium can detect
        # when the current page disappears.
        old_first_quote = driver.find_element(
            By.CSS_SELECTOR,
            "div.quote"
        )

        next_button = next_buttons[0]

        # Scroll to the Next button.
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            next_button
        )

        # Click the Next button using JavaScript.
        driver.execute_script(
            "arguments[0].click();",
            next_button
        )

        # Wait until the old page content is replaced.
        wait.until(
            EC.staleness_of(old_first_quote)
        )

        page_number += 1


    # -----------------------------------------------------
    # REMOVE DUPLICATE RECORDS
    # -----------------------------------------------------

    unique_quotes = []

    seen_records = set()

    for record in all_quotes:

        unique_key = (
            record["Quote"],
            record["Author"]
        )

        if unique_key not in seen_records:
            seen_records.add(unique_key)
            unique_quotes.append(record)


    # -----------------------------------------------------
    # CREATE PANDAS DATAFRAME
    # -----------------------------------------------------

    dataframe = pd.DataFrame(unique_quotes)

    print("\n---------------------------------")
    print("SCRAPING RESULTS")
    print("---------------------------------")
    print(dataframe)

    print(f"\nTotal records: {len(dataframe)}")


    # -----------------------------------------------------
    # SAVE THE DATA INTO CSV
    # -----------------------------------------------------

    if not dataframe.empty:

        dataframe.to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        print("\nScraping completed successfully.")
        print(f"CSV saved at:\n{OUTPUT_FILE}")

    else:
        print("\nNo data was extracted.")


except TimeoutException:
    print("\nWebsite elements took too long to load.")
    print("Check your internet connection and selectors.")

except ValueError as error:
    print(f"\nURL error: {error}")

except Exception as error:
    print(f"\nMain program error: {error}")


finally:
    # -----------------------------------------------------
    # CLOSE THE BROWSER
    # -----------------------------------------------------

    print("\nClosing browser...")
    driver.quit()   