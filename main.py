import time
import csv
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
        'sezona': input("sezona: ").strip().capitalize(),
        'razotajs': input("ražotājs: ").strip()
    }
    filters = {k: v for k, v in filters.items() if v}
    if not filters:
        print("\nvisi lauki nedrikst but tuksi")
        return get_user_input()

    return filters

def select_dropdown(driver, label_text, value):
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
        time.sleep(1)
        return True
    except Exception:
        print(f"error {label_text}")
        return False

def extract_results(driver):
    products = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.products li.product"))
    )
    results = []
    for product in products:
        try:
            title = product.find_element(By.CSS_SELECTOR, '.woocommerce-loop-product__title').text.strip()
            price = product.find_element(By.CSS_SELECTOR, '.price span.woocommerce-Price-amount').text.strip()
            results.append({'Title': title, 'Price': format_price(price)})
        except Exception:
            print("error")
    return results

def format_price(price):
    try:
        numeric_price = ''.join(filter(str.isdigit, price))
        return "{:,.2f}".format(int(numeric_price) / 100)
    except ValueError:
        return price

def save_to_csv(data, filename='results.csv'):
    if not data:
        print("error")
        return

    file_exists = False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())

        if not file_exists:
            writer.writeheader()

        writer.writerows(data)

    print(f"rezultati saglabati {filename}")

def main():
    user_filter = get_user_input()

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://mmkriepas.lv/riepas/")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'form.mmk-filter'))
        )

        success = True
        if 'platums' in user_filter:
            success = select_dropdown(driver, 'Platums', user_filter['platums'])
        if success and 'augstums' in user_filter:
            success = select_dropdown(driver, 'Augstums', user_filter['augstums'])
        if success and 'diametrs' in user_filter:
            success = select_dropdown(driver, 'Diametrs', user_filter['diametrs'])
        if success and 'sezona' in user_filter:
            success = select_dropdown(driver, 'Sezona', user_filter['sezona'])
        if success and 'razotajs' in user_filter:
            success = select_dropdown(driver, 'Ražotājs', user_filter['razotajs'])

        if success:
            search_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[type="submit"].mmk-product-filters__search-button'))
            )
            search_btn.click()

            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.products li.product"))
            )

            time.sleep(3)

            results = extract_results(driver)
            save_to_csv(results)
        else:
            print("filter error")

    except Exception:
        print("error")

    finally:
        input("press enter to exit...")

if __name__ == "__main__":
    main()
