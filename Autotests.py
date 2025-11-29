# Лабораторная работа 9 - CI/CD тестирование
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import sys

def setup_driver():
    """Настройка драйвера для CI/CD"""
    chrome_options = Options()
    
    # Обязательные опции для GitHub Actions
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Используем системный ChromeDriver
    driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=chrome_options)
    return driver

def test_basic_functionality():
    """Упрощенный тест для проверки работы в CI/CD"""
    print("🚀 Запуск базового теста в CI/CD...")
    
    driver = setup_driver()
    
    try:
        # Простой тест - открываем страницу и проверяем основные элементы
        driver.get("https://e.mospolytech.ru/")
        print("✓ Страница загружена")
        
        # Проверяем заголовок
        title = driver.title
        print(f"✓ Заголовок страницы: {title}")
        
        # Проверяем наличие основных элементов
        inputs = driver.find_elements(By.TAG_NAME, "input")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        links = driver.find_elements(By.TAG_NAME, "a")
        
        print(f"✓ Найдено элементов: {len(inputs)} полей, {len(buttons)} кнопок, {len(links)} ссылок")
        
        # Делаем скриншот для отладки
        driver.save_screenshot('page_screenshot.png')
        print("✓ Скриншот сохранен")
        
        # Базовая проверка - если страница загрузилась и есть элементы, считаем успехом
        if len(inputs) > 0 or len(buttons) > 0:
            print("✅ ТЕСТ ПРОЙДЕН: Страница загружена, элементы найдены")
            return True
        else:
            print("❌ ТЕСТ ПРОВАЛЕН: Не найдены элементы на странице")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при выполнении теста: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    print("🎯 ЛАБОРАТОРНАЯ РАБОТА 9: CI/CD ТЕСТИРОВАНИЕ")
    print("=" * 60)
    
    success = test_basic_functionality()
    
    if success:
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("🎉 CI/CD настроен корректно!")
        sys.exit(0)
    else:
        print("\n❌ ТЕСТЫ ПРОВАЛЕНЫ!")
        sys.exit(1)

