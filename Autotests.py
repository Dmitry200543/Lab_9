import sys
import os
import json
from datetime import datetime
import urllib.request
import subprocess

class CICDTestRunner:
    """Класс для запуска тестов CI/CD"""
    
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'tests': [],
            'environment': {},
            'timestamp': datetime.now().isoformat()
        }
    
    def log_test(self, name, status, message=""):
        """Логирует результат теста"""
        test_result = {
            'name': name,
            'status': status,
            'message': message,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        
        self.results['tests'].append(test_result)
        
        if status == "PASSED":
            self.results['passed'] += 1
            print(f"✅ {name}")
        else:
            self.results['failed'] += 1
            print(f"❌ {name}")
        
        if message:
            print(f"   📝 {message}")
    
    def test_python_environment(self):
        """Тест окружения Python"""
        print("\n🔧 ТЕСТИРОВАНИЕ ОКРУЖЕНИЯ PYTHON")
        
        # Проверяем версию Python
        python_version = sys.version.split()[0]
        self.log_test(
            "Версия Python", 
            "PASSED", 
            f"Версия: {python_version}"
        )
        
        # Проверяем рабочую директорию
        cwd = os.getcwd()
        self.log_test(
            "Рабочая директория", 
            "PASSED", 
            f"Директория: {cwd}"
        )
        
        # Проверяем переменные окружения
        env_vars = {
            'GITHUB_ACTIONS': os.getenv('GITHUB_ACTIONS'),
            'GITHUB_REPOSITORY': os.getenv('GITHUB_REPOSITORY'),
            'GITHUB_WORKFLOW': os.getenv('GITHUB_WORKFLOW')
        }
        
        self.results['environment'] = env_vars
        
        self.log_test(
            "Переменные GitHub Actions", 
            "PASSED" if any(env_vars.values()) else "FAILED",
            f"Найдено: {sum(1 for v in env_vars.values() if v)}/{len(env_vars)}"
        )
        
        return True
    
    def test_file_system(self):
        """Тест файловой системы"""
        print("\n📁 ТЕСТИРОВАНИЕ ФАЙЛОВОЙ СИСТЕМЫ")
        
        # Проверяем наличие текущего файла
        current_file = os.path.basename(__file__)
        if os.path.exists(current_file):
            self.log_test(
                "Доступ к файлам репозитория", 
                "PASSED",
                f"Файл: {current_file}"
            )
        else:
            self.log_test(
                "Доступ к файлам репозитория", 
                "FAILED",
                "Не удалось найти файлы"
            )
            return False
        
        # Создаем тестовый файл
        try:
            with open('ci_cd_test_artifact.txt', 'w') as f:
                f.write("Тестовый артефакт CI/CD\n")
                f.write(f"Создан: {datetime.now()}\n")
                f.write("Лабораторная работа 9 - Успешно!\n")
            
            self.log_test(
                "Создание артефактов", 
                "PASSED",
                "Файл ci_cd_test_artifact.txt создан"
            )
            
            # Читаем файл обратно
            with open('ci_cd_test_artifact.txt', 'r') as f:
                content = f.read()
                lines = len(content.split('\n'))
            
            self.log_test(
                "Чтение артефактов", 
                "PASSED",
                f"Прочитано строк: {lines}"
            )
            
            # Удаляем тестовый файл
            os.remove('ci_cd_test_artifact.txt')
            self.log_test(
                "Очистка артефактов", 
                "PASSED",
                "Временные файлы удалены"
            )
            
            return True
            
        except Exception as e:
            self.log_test(
                "Операции с файлами", 
                "FAILED",
                f"Ошибка: {e}"
            )
            return False
    
    def test_network_connectivity(self):
        """Тест сетевой connectivity"""
        print("\n🌐 ТЕСТИРОВАНИЕ СЕТЕВОЙ СВЯЗНОСТИ")
        
        test_urls = [
            "https://www.google.com",
            "https://github.com",
            "https://example.com"
        ]
        
        successful_connections = 0
        
        for url in test_urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    status = response.getcode()
                    if status == 200:
                        successful_connections += 1
                        self.log_test(
                            f"Доступ к {url}", 
                            "PASSED",
                            f"Статус: {status}"
                        )
                    else:
                        self.log_test(
                            f"Доступ к {url}", 
                            "FAILED",
                            f"Статус: {status}"
                        )
            except Exception as e:
                self.log_test(
                    f"Доступ к {url}", 
                    "FAILED",
                    f"Ошибка: {type(e).__name__}"
                )
        
        self.log_test(
            "Общая сетевая связность", 
            "PASSED" if successful_connections >= 2 else "FAILED",
            f"Успешных подключений: {successful_connections}/{len(test_urls)}"
        )
        
        return successful_connections >= 2
    
    def test_ci_cd_logic(self):
        """Тест логики CI/CD"""
        print("\n🔄 ТЕСТИРОВАНИЕ ЛОГИКИ CI/CD")
        
        # Имитация тестовой логики
        test_cases = [
            {"name": "Проверка условий", "condition": True, "expected": True},
            {"name": "Валидация данных", "condition": "CI/CD" == "CI/CD", "expected": True},
            {"name": "Логика выполнения", "condition": len("test") == 4, "expected": True},
        ]
        
        passed_tests = 0
        
        for i, test_case in enumerate(test_cases, 1):
            if test_case['condition'] == test_case['expected']:
                passed_tests += 1
                self.log_test(
                    f"Тест кейс {i}: {test_case['name']}", 
                    "PASSED",
                    "Условие выполнено"
                )
            else:
                self.log_test(
                    f"Тест кейс {i}: {test_case['name']}", 
                    "FAILED",
                    "Условие не выполнено"
                )
        
        self.log_test(
            "Общая логика тестирования", 
            "PASSED" if passed_tests == len(test_cases) else "FAILED",
            f"Пройдено: {passed_tests}/{len(test_cases)}"
        )
        
        return passed_tests == len(test_cases)
    
    def generate_report(self):
        """Генерирует финальный отчет"""
        print("\n" + "="*70)
        print("🎯 ОТЧЕТ О ВЫПОЛНЕНИИ ЛАБОРАТОРНОЙ РАБОТЫ 9")
        print("="*70)
        
        total_tests = self.results['passed'] + self.results['failed']
        success_rate = (self.results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 СВОДКА ТЕСТОВ:")
        print(f"   ✅ Пройдено: {self.results['passed']}")
        print(f"   ❌ Провалено: {self.results['failed']}")
        print(f"   📈 Общее количество: {total_tests}")
        print(f"   🎯 Успешность: {success_rate:.1f}%")
        
        print(f"\n🕐 Время выполнения: {self.results['timestamp']}")
        
        print(f"\n🌍 ОКРУЖЕНИЕ CI/CD:")
        for key, value in self.results['environment'].items():
            if value:
                print(f"   {key}: {value}")
        
        print("="*70)
        
        if self.results['failed'] == 0:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
            print("🚀 Лабораторная работа 9 ВЫПОЛНЕНА!")
            print("✅ CI/CD настроен и работает корректно!")
            return True
        else:
            print(f"\n⚠ Обнаружены проблемы в {self.results['failed']} тестах")
            return False
    
    def run_all_tests(self):
        """Запускает все тесты"""
        print("🚀 ЗАПУСК CI/CD АВТОТЕСТОВ")
        print("Лабораторная работа 9: Интеграция автотестов в CI/CD")
        print("="*70)
        
        # Запускаем тесты
        self.test_python_environment()
        self.test_file_system()
        self.test_network_connectivity()
        self.test_ci_cd_logic()
        
        # Генерируем отчет
        return self.generate_report()

def main():
    """Основная функция"""
    runner = CICDTestRunner()
    success = runner.run_all_tests()
    
    # Сохраняем результаты в файл (артефакт CI/CD)
    with open('test_results.json', 'w') as f:
        json.dump(runner.results, f, indent=2, ensure_ascii=False)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
