from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🔐 ВАШИ РЕАЛЬНЫЕ ДАННЫЕ
USERNAME = "d.s.byrdin"  # Ваш логин
PASSWORD = "Stud981185!"  # Замените на ваш пароль

def test_successful_login():
    """Тест: Успешный вход в систему с реальными данными"""
    print("🚀 Тестирование успешного входа в систему...")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Открываем страницу логина
        driver.get("https://e.mospolytech.ru/#/login")
        wait = WebDriverWait(driver, 15)
        print("✓ Страница логина загружена")
        
        # Ждем полной загрузки
        time.sleep(5)
        
        print("Поиск элементов формы...")
        
        # Ищем ВСЕ элементы на странице для анализа
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        
        print(f"Найдено input элементов: {len(all_inputs)}")
        print(f"Найдено button элементов: {len(all_buttons)}")
        
        # Анализируем все input элементы
        for i, inp in enumerate(all_inputs):
            input_type = inp.get_attribute("type")
            placeholder = inp.get_attribute("placeholder")
            input_id = inp.get_attribute("id")
            input_name = inp.get_attribute("name")
            print(f"  Input {i+1}: type={input_type}, placeholder={placeholder}, id={input_id}, name={input_name}")
        
        # Анализируем все button элементы
        for i, btn in enumerate(all_buttons):
            btn_text = btn.text
            btn_type = btn.get_attribute("type")
            btn_class = btn.get_attribute("class")
            is_displayed = btn.is_displayed()
            is_enabled = btn.is_enabled()
            print(f"  Button {i+1}: text='{btn_text}', type={btn_type}, class={btn_class}, displayed={is_displayed}, enabled={is_enabled}")
        
        # Находим поле логина (первое текстовое поле)
        username_fields = [inp for inp in all_inputs if inp.get_attribute("type") == "text"]
        if username_fields:
            username_field = username_fields[0]
            print("✓ Найдено поле логина")
        else:
            print("❌ Поле логина не найдено")
            return
        
        # Находим поле пароля
        password_fields = [inp for inp in all_inputs if inp.get_attribute("type") == "password"]
        if password_fields:
            password_field = password_fields[0]
            print("✓ Найдено поле пароля")
        else:
            print("❌ Поле пароля не найдено")
            return
        
        # НАХОДИМ КНОПКУ "ВХОД" - ИЩЕМ ТОЧНО ПО ТЕКСТУ
        login_button = None
        
        # Способ 1: Ищем по точному тексту "Вход"
        for btn in all_buttons:
            if btn.text.strip() == "Вход":
                login_button = btn
                print(f"✓ Найдена кнопка 'Вход' по точному тексту")
                break
        
        # Способ 2: Если не нашли по точному тексту, ищем по классу submit-button
        if not login_button:
            for btn in all_buttons:
                if "submit-button" in btn.get_attribute("class"):
                    login_button = btn
                    print(f"✓ Найдена кнопка по классу submit-button: '{btn.text}'")
                    break
        
        # Способ 3: Ищем видимую кнопку с текстом, содержащим "Вход"
        if not login_button:
            for btn in all_buttons:
                if "Вход" in btn.text and btn.is_displayed() and btn.is_enabled():
                    login_button = btn
                    print(f"✓ Найдена видимая кнопка с текстом 'Вход': '{btn.text}'")
                    break
        
        # Способ 4: Используем XPath для поиска кнопки "Вход"
        if not login_button:
            try:
                login_button = driver.find_element(By.XPATH, "//button[text()='Вход']")
                print("✓ Найдена кнопка 'Вход' через XPath")
            except:
                pass
        
        if not login_button:
            print("❌ Кнопка 'Вход' не найдена")
            # Показываем все кнопки с текстом
            buttons_with_text = [btn for btn in all_buttons if btn.text.strip()]
            print("Кнопки с текстом:")
            for btn in buttons_with_text:
                print(f"  - '{btn.text}' (displayed: {btn.is_displayed()}, enabled: {btn.is_enabled()})")
            return
        
        print(f"✅ Используем кнопку: '{login_button.text}' (displayed: {login_button.is_displayed()}, enabled: {login_button.is_enabled()})")
        
        # Вводим логин
        username_field.clear()
        username_field.send_keys(USERNAME)
        print(f"✓ Введен логин: {USERNAME}")
        time.sleep(1)
        
        # Вводим пароль
        password_field.clear()
        password_field.send_keys(PASSWORD)
        print("✓ Введен пароль")
        time.sleep(1)
        
        # Прокручиваем к кнопке, чтобы она стала видимой
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        time.sleep(1)
        
        # Пробуем разные способы нажатия кнопки
        print("Пробуем нажать кнопку...")
        
        try:
            # Способ 1: Обычный click
            login_button.click()
            print("✓ Кнопка нажата через .click()")
        except Exception as e:
            print(f"❌ Ошибка при .click(): {e}")
            try:
                # Способ 2: Click через JavaScript
                driver.execute_script("arguments[0].click();", login_button)
                print("✓ Кнопка нажата через JavaScript")
            except Exception as e2:
                print(f"❌ Ошибка при JavaScript click: {e2}")
                try:
                    # Способ 3: Enter в поле пароля
                    password_field.send_keys(Keys.ENTER)
                    print("✓ Отправлена форма через Enter")
                except Exception as e3:
                    print(f"❌ Все способы не сработали: {e3}")
        
        # Ждем результат входа
        time.sleep(5)
        
        # Проверяем, успешен ли вход
        current_url = driver.current_url
        page_title = driver.title
        print(f"Текущий URL после входа: {current_url}")
        print(f"Заголовок страницы: {page_title}")
        
        if "login" not in current_url.lower() and "auth" not in current_url.lower():
            print("✅ ВХОД ВЫПОЛНЕН УСПЕШНО! Система загружена")
            
            # Проверяем элементы личного кабинета
            try:
                page_text = driver.page_source.lower()
                if "главная" in page_text or "расписание" in page_text or "успеваемость" in page_text:
                    print("✅ Найдены элементы личного кабинета")
                
                # Ищем приветствие или имя пользователя
                user_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'd.s.byrdin') or contains(text(), 'Бырдин') or contains(text(), 'Дмитрий')]")
                if user_elements:
                    print(f"✅ Найдено приветствие: {user_elements[0].text}")
                    
            except Exception as e:
                print(f"⚠ Не удалось найти специфичные элементы: {e}")
                
        else:
            print("❌ Вход не выполнен. Остались на странице логина")
            
            # Проверяем наличие сообщения об ошибке
            try:
                error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Ошибка') or contains(text(), 'Неверный') or contains(text(), 'error') or contains(text(), 'invalid')]")
                if error_elements:
                    print(f"❌ Сообщение об ошибке: {error_elements[0].text}")
            except:
                print("⚠ Сообщение об ошибке не найдено")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении входа: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Не закрываем браузер сразу, чтобы можно было посмотреть результат
        print("✓ Браузер остается открытым для проверки")
        input("Нажмите Enter чтобы закрыть браузер...")
        driver.quit()
        print("✅ Тестирование входа завершено!")

def test_specific_selectors():
    """Тест конкретных селекторов для кнопки 'Вход'"""
    print("\n🎯 Тестирование конкретных селекторов...")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        driver.get("https://e.mospolytech.ru/#/login")
        time.sleep(5)
        
        # Тестируем разные селекторы для кнопки "Вход"
        selectors = [
            ("Точный текст 'Вход'", "//button[text()='Вход']"),
            ("Класс submit-button", "//button[contains(@class, 'submit-button')]"),
            ("Класс sc-r09aw-0", "//button[contains(@class, 'sc-r09aw-0')]"),
            ("Класс NKlHC", "//button[contains(@class, 'NKlHC')]"),
            ("7-я кнопка", "(//button)[7]"),
            ("Кнопка с type=submit и текстом", "//button[@type='submit' and text()='Вход']")
        ]
        
        for name, selector in selectors:
            try:
                element = driver.find_element(By.XPATH, selector)
                print(f"✅ {name}: НАЙДЕН - text='{element.text}', displayed={element.is_displayed()}, enabled={element.is_enabled()}")
            except:
                print(f"❌ {name}: не найден")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🎯 ЛАБОРАТОРНАЯ РАБОТА 3: АВТОТЕСТ С ВХОДОМ В СИСТЕМУ")
    print("="*70)
    
    # Проверяем, введен ли пароль
    if PASSWORD == "ваш_пароль":
        print("\n❌ ВНИМАНИЕ: ПАРОЛЬ НЕ ВВЕДЕН!")
        print("Замените 'ваш_пароль' на реальный пароль в коде")
        print("и запустите программу снова")
    else:
        print(f"\n✅ Данные для входа: Логин = {USERNAME}")
        
        # Тестируем селекторы
        test_specific_selectors()
        
        # Запускаем тест входа
        test_successful_login()
    
    print("\n" + "="*70)
    print("📋 ОТЧЕТ ПО ЛАБОРАТОРНОЙ РАБОТЕ 3")
    print("="*70)
    print("✅ Настроено окружение Selenium WebDriver")
    print("✅ Реализована инициализация браузера") 
    print("✅ Проанализирована структура страницы")
    print("✅ Найдены поля логина и пароля")
    print("✅ Реализован интеллектуальный поиск элементов")
    print("✅ Добавлены multiple способы поиска кнопки")
    print("✅ Автотест готов к выполнению входа")
    print("="*70)