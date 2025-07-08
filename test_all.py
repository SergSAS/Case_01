#!/usr/bin/env python3
"""
Полный тест функциональности проекта LLM Text Summarization Analysis.
Проверяет все основные компоненты и генерирует отчеты.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_section(title: str):
    """Печатает заголовок секции."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def check_dependencies():
    """Проверяет наличие зависимостей."""
    print_section("CHECKING DEPENDENCIES")
    
    try:
        import groq
        print("[OK] groq library installed")
    except ImportError:
        print("[ERROR] groq library not found")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Проверка переменной окружения
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        print("[OK] GROQ_API_KEY environment variable set")
    else:
        print("[WARNING] GROQ_API_KEY not set - some tests will be skipped")
    
    return True


def check_file_structure():
    """Проверяет структуру файлов проекта."""
    print_section("CHECKING FILE STRUCTURE")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "LICENSE",
        "CONTRIBUTING.md",
        ".gitignore",
        "env.example",
        "groq_new_prompt.py",
        "generate_report.py",
        "view_report.py",
        "src/__init__.py",
        "src/llm_analyzer.py",
        "data/source_article.txt",
        "reports/FINAL_STRUCTURED_REPORT.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[MISSING] {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n[ERROR] Missing {len(missing_files)} required files")
        return False
    
    print(f"\n[OK] All {len(required_files)} required files found")
    return True


def test_analyzer():
    """Тестирует модуль анализатора."""
    print_section("TESTING LLM ANALYZER")
    
    try:
        from src.llm_analyzer import LLMAnalyzer
        
        analyzer = LLMAnalyzer()
        print("[OK] LLMAnalyzer imported successfully")
        
        # Тест базовых методов
        test_text = "This is a test summary with about ten words."
        coverage = analyzer.calculate_coverage(test_text, ["test", "summary"])
        print(f"[OK] Coverage calculation: {coverage}%")
        
        coherence = analyzer.calculate_coherence(test_text)
        print(f"[OK] Coherence calculation: {coherence}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Analyzer test failed: {str(e)}")
        return False


def test_report_generator():
    """Тестирует генератор отчетов."""
    print_section("TESTING REPORT GENERATOR")
    
    try:
        # Импорт без выполнения
        import sys
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("generate_report", "generate_report.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["generate_report"] = module
        spec.loader.exec_module(module)
        
        generator = module.ReportGenerator()
        print("[OK] ReportGenerator imported successfully")
        
        # Тест базовых методов
        test_summaries = {
            'claude': "Test Claude summary with exactly ten words here now.",
            'groq': "Test Groq summary with different word count here."
        }
        
        word_count = generator.count_words(test_summaries['claude'])
        print(f"[OK] Word count: {word_count}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Report generator test failed: {str(e)}")
        return False


def test_groq_script():
    """Тестирует скрипт Groq (если API ключ доступен)."""
    print_section("TESTING GROQ SCRIPT")
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("[SKIP] GROQ_API_KEY not set - skipping API test")
        return True
    
    try:
        # Запуск скрипта
        result = subprocess.run(
            [sys.executable, "groq_new_prompt.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("[OK] Groq script executed successfully")
            
            # Проверка созданных файлов
            if os.path.exists("results/groq_new_result.json"):
                print("[OK] JSON result file created")
            if os.path.exists("results/groq_new_summary.txt"):
                print("[OK] Summary text file created")
                
            return True
        else:
            print(f"[ERROR] Groq script failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Groq script timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Groq script test failed: {str(e)}")
        return False


def check_code_quality():
    """Проверяет качество кода."""
    print_section("CHECKING CODE QUALITY")
    
    python_files = [
        "groq_new_prompt.py",
        "generate_report.py", 
        "view_report.py",
        "src/llm_analyzer.py"
    ]
    
    issues = 0
    
    for file_path in python_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Базовые проверки PEP8
            lines = content.split('\n')
            
            # Проверка docstring
            has_docstring = False
            
            # Ищем docstring в первых нескольких строках (после shebang)
            for line in lines[:5]:
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    has_docstring = True
                    break
            
            if not has_docstring:
                print(f"[WARNING] {file_path}: Missing module docstring")
                issues += 1
            else:
                print(f"[OK] {file_path}: Has module docstring")
            
            # Проверка длинных строк
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 100]
            if long_lines:
                print(f"[WARNING] {file_path}: Lines too long: {len(long_lines)} lines")
                issues += 1
            else:
                print(f"[OK] {file_path}: Line length OK")
    
    if issues == 0:
        print(f"\n[OK] Code quality check passed")
    else:
        print(f"\n[WARNING] Found {issues} code quality issues")
    
    return issues == 0


def generate_final_report():
    """Генерирует финальный отчет."""
    print_section("GENERATING FINAL REPORT")
    
    try:
        result = subprocess.run(
            [sys.executable, "generate_report.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("[OK] Report generated successfully")
            print(result.stdout)
            return True
        else:
            print(f"[ERROR] Report generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Report generation test failed: {str(e)}")
        return False


def main():
    """Главная функция тестирования."""
    print_section("LLM TEXT SUMMARIZATION ANALYSIS - FULL TEST")
    
    tests = [
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("LLM Analyzer", test_analyzer),
        ("Report Generator", test_report_generator),
        ("Code Quality", check_code_quality),
        ("Groq Script", test_groq_script),
        ("Final Report", generate_final_report)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n>>> Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"[PASS] {test_name}")
            else:
                print(f"[FAIL] {test_name}")
        except Exception as e:
            print(f"[ERROR] {test_name}: {str(e)}")
    
    print_section("TEST RESULTS")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Project is ready for publication.")
        return 0
    else:
        print(f"\n[WARNING] {total-passed} tests failed. Please fix issues before publication.")
        return 1


if __name__ == "__main__":
    exit(main()) 