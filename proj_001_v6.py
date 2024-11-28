####################################################################
# Step 1: Initialize Selenium WebDriver
####################################################################
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set options for Firefox WebDriver
options = webdriver.FirefoxOptions()

# Start browser maximized
options.add_argument("--start-maximized")

# Override the user agent string
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0")

# Initialize WebDriver with the path to geckodriver
driver = webdriver.Firefox(executable_path='/home/train/web_scraping/Selenium/geckodriver', options=options)

####################################################################
# Step 2: Navigate to the website
####################################################################
import time
SLEEP_TIME = 2

# Target URL
url = "https://www.commonsensemedia.org"
driver.get(url)
time.sleep(SLEEP_TIME)

####################################################################
# Step 3: Interact with the first menu
####################################################################

# Find elements in the "Best Movie Lists" menu
btn_element = driver.find_elements(By.XPATH, "//ul[@class='menu']//a[contains(text(), 'Best Movie Lists')]")

# Select the first element in the list
first_element = btn_element[0]
time.sleep(SLEEP_TIME)

# Scroll the element into view
driver.execute_script("arguments[0].scrollIntoView(true);", first_element)
time.sleep(SLEEP_TIME)

SLEEP_TIME_5 = 5
# Click the element using JavaScript
driver.execute_script("arguments[0].click();", first_element)
time.sleep(SLEEP_TIME_5)

####################################################################
# Step 4: Interact with filters
####################################################################

# Locate the first filter button
button = driver.find_element(By.XPATH, '//*[@id="top-picks-best-lists-filter"]/div/button')

time.sleep(SLEEP_TIME_5)
# Scroll the element into view
driver.execute_script("arguments[0].scrollIntoView(true);", button)

time.sleep(SLEEP_TIME_5)
# Click the button using JavaScript
driver.execute_script("arguments[0].click();", button)

time.sleep(SLEEP_TIME_5)
# Find the "Big Kids" button using its XPath
big_kids_button = driver.find_element(By.XPATH, "//*[@id='top-picks-best-lists-filter']/div/div/button[4]")

time.sleep(SLEEP_TIME_5)
# Scroll the element into view
driver.execute_script("arguments[0].scrollIntoView(true);", big_kids_button)
time.sleep(SLEEP_TIME_5)

# Click the "Big Kids" button
driver.execute_script("arguments[0].click();", big_kids_button)
time.sleep(SLEEP_TIME_5)

####################################################################
# Step 5: Scrape pages
####################################################################
import time
import pandas as pd
from selenium.webdriver.common.by import By

SLEEP_TIME = 10
SLEEP_TIME_2 = 2

# Initialize an empty list to store scraped data
data = []

for i in range(1, 10):
    try:
        # Locate the "Next" button using its XPath and click it
        next_button = driver.find_element(By.XPATH, f'//li[contains(@class, "pagination__link")]//button[@aria-label="Goto page {i}"]')
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", next_button)
        next_button.click()
        time.sleep(SLEEP_TIME_2)

        next_button = driver.find_element(By.XPATH, f'//li[contains(@class, "pagination__link")]//button[@aria-label="Goto page {i}"]')
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", next_button)
        next_button.click()

        time.sleep(SLEEP_TIME)

        # Locate the sublist elements
        sub_list_xpath = "//div[@class='col']//h4"
        sub_list_elements = driver.find_elements(By.XPATH, sub_list_xpath)

        # Print the total number of elements
        print("Total elements:", len(sub_list_elements))
        for element in sub_list_elements:
            header_text = element.text  # Extract the text of the element
            sub_list_url = None  # Default the URL to None

            # Attempt to extract the inner link
            try:
                sub_list_url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
            except Exception as e:
                print("Not found tag URL. Error:", str(e))

            # Append the extracted data to the list
            data.append({"Header": header_text, "URL": sub_list_url})  # Use correct variable names

        time.sleep(SLEEP_TIME)
    except Exception as e:
        print(f"Error on page {i}: {str(e)}")

# Create a DataFrame from the scraped data
if data:
    df = pd.DataFrame(data)
else:
    print("Data list is empty; no DataFrame created.")
    df = pd.DataFrame()

print("\nGenerated DataFrame:")
print(df)

# Save the DataFrame
if not df.empty:
    # Save as an Excel file
    excel_file = "output_data.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"DataFrame saved as Excel: {excel_file}")

    # Save as a JSON file
    json_file = "output_data.json"
    df.to_json(json_file, orient="records", lines=True, force_ascii=False)
    print(f"DataFrame saved as JSON: {json_file}")
else:
    print("DataFrame is empty; nothing to save.")

# Close the browser
driver.quit()
