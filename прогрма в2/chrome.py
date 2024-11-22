import time
import pyperclip
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, NoSuchFrameException

def switch_to_frame(driver):
    """Функція для переключення на перший доступний фрейм"""
    try:
        # Зачекаємо додатковий час для завантаження фреймів
        time.sleep(5)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"Знайдено {len(iframes)} фрейм(и). Перемикаємось на перший.")
            driver.switch_to.frame(iframes[0])  # Перемикання на перший фрейм
        else:
            print("Фрейми не знайдено.")
    except NoSuchFrameException:
        print("Помилка: не вдалося перемкнутися на фрейм.")

def save_text_to_file(text, filename="visible_text.txt"):
    """Функція для збереження тексту у файл, перезаписуючи попередній текст"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Текст збережено у файл {filename}!")

def get_visible_text(driver):
    # Перевіряємо, чи є на сторінці фрейми і перемикаємося
    switch_to_frame(driver)

    # Збираємо весь видимий текст
    elements = driver.find_elements(By.XPATH, "//*[not(self::script) and not(self::style)]")
    visible_text = []

    # Retry mechanism to handle stale elements
    for element in elements:
        retry_count = 3  # Try 3 times to avoid stale elements
        while retry_count > 0:
            try:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        visible_text.append(text)
                break
            except StaleElementReferenceException:
                retry_count -= 1
                # Re-fetch elements in case of page changes
                elements = driver.find_elements(By.XPATH, "//*[not(self::script) and not(self::style)]")

    # Об'єднуємо текст у великий блок
    full_text = "\n".join(visible_text)

    # Зберігаємо текст у файл, перезаписуючи старий
    save_text_to_file(full_text)

def main_loop():
    # Налаштування Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Запускаємо драйвер
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Головний цикл програми
        while True:
            print("Натисніть Ctrl + Alt + A, щоб зчитати URL з буферу обміну або 'Ctrl + C' для виходу.")

            # Очікування на комбінацію клавіш Ctrl + Alt + A
            keyboard.wait('ctrl+alt+a')

            # Зчитуємо URL з буферу обміну
            url = pyperclip.paste()
            print(f"URL зчитано з буферу обміну: {url}")

            # Відкриваємо новий сайт за URL
            driver.get(url)

            # Зачекаємо кілька секунд для завантаження сторінки
            time.sleep(5)

            # Збираємо видимий текст і зберігаємо його у файл
            get_visible_text(driver)

    except KeyboardInterrupt:
        # Дозволяємо користувачеві завершити роботу через Ctrl + C
        print("Програму завершено.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main_loop()

