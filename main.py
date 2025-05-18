import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_user_input():
    filters = {
        'platums': input("platums: ").strip(),
        'augstums': input("augstums: ").strip(),
        'diametrs': input("diametrs: ").strip(),
        'razotajs': input("ražotājs: ").strip(),
        'sezona': input("sezona: ").strip().capitalize()
    }
    filters = {k: v for k, v in filters.items() if v}

    if not filters:
        print("\nvisi lauki nevar but tukši!")
        return get_user_input()

    return filters

def select_dropdown(driver, label_text, value):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            label_xpath = f'//label[contains(text(), "{label_text}")]/following-sibling::span[contains(@class, "select2-container")]'
            select_span = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, label_xpath)))
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
            time.sleep(1)
            return
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(2)

def main():
    user_filter = get_user_input()
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        season = user_filter.get('sezona', '')
        if season == 'Ziema':
            url = "https://mmkriepas.lv/riepas/ziemas-riepas/"
        elif season == 'Vissezonas':
            url = "https://mmkriepas.lv/riepas/vissezonas-riepas/"
        elif season == 'Vasara':
            url = "https://mmkriepas.lv/riepas/vasaras-riepas/"
        else:
            url = "https://mmkriepas.lv/riepas/"

        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form.mmk-filter'))
        )

        if 'platums' in user_filter:
            select_dropdown(driver, 'Platums', user_filter['platums'])
        if 'augstums' in user_filter:
            select_dropdown(driver, 'Augstums', user_filter['augstums'])
        if 'diametrs' in user_filter:
            select_dropdown(driver, 'Diametrs', user_filter['diametrs'])
        if 'razotajs' in user_filter:
            select_dropdown(driver, 'Ražotājs', user_filter['razotajs'])

        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"].mmk-product-filters__search-button'))
        )
        search_btn.click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.mmk-product-list'))
        )
        print("success")


    except Exception as e:
        print(f"error: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()