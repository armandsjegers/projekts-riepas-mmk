import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_filter = {
    'platums': '205',
    'augstums': '55',
    'diametrs': 'R16',
    'razotajs': 'Michelin',
}

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://mmkriepas.lv/riepas/vasaras-riepas/")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'form.mmk-filter'))
    )

    def select_dropdown(label_text, value):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                label_xpath = f'//label[contains(text(), "{label_text}")]/following-sibling::span[contains(@class, "select2-container")]'
                select_span = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, label_xpath))
                )
                select_span.click()

                dropdown = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "span.select2-dropdown"))
                )

                search_input = WebDriverWait(dropdown, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
                )
                search_input.clear()
                search_input.send_keys(value)
                time.sleep(1)

                option_xpath = f'//li[contains(@class, "select2-results__option") and contains(., "{value}")]'
                option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option.click()
                print(f"✅ Selected {label_text}: {value}")
                time.sleep(1)
                return
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                print(f"⚠️ Attempt {attempt + 1} failed for {label_text}. Retrying...")
                time.sleep(2)

    select_dropdown('Platums', user_filter['platums'])
    select_dropdown('Augstums', user_filter['augstums'])
    select_dropdown('Diametrs', user_filter['diametrs'])

    if user_filter['razotajs']:
        select_dropdown('Ražotājs', user_filter['razotajs'])

    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].mmk-product-filters__search-button'))
    )
    search_btn.click()
    print("Search triggered.")

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.mmk-product-list'))
    )
    print("Results loaded successfully!")
    time.sleep(10)

finally:
    driver.quit()