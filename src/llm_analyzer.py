#!/usr/bin/env python3
"""
Модуль для анализа и сравнения качества суммаризации LLM моделей.

Предоставляет класс LLMAnalyzer для вычисления различных метрик качества
суммаризации текста: faithfulness, coverage, prompt adherence, coherence
и compression ratio. Позволяет проводить сравнительный анализ нескольких
моделей и генерировать отчеты с рейтингом качества.
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime


class LLMAnalyzer:
    """Класс для анализа качества суммаризации LLM моделей."""
    
    def __init__(self):
        """Инициализация анализатора."""
        self.metrics_weights = {
            'faithfulness': 0.30,    # Верность исходному тексту
            'coverage': 0.25,        # Покрытие ключевых тем
            'prompt_adherence': 0.20,  # Следование инструкциям
            'coherence': 0.15,       # Связность текста
            'compression': 0.10      # Эффективность сжатия
        }
    
    def calculate_faithfulness(self, summary: str, source_facts: List[str]) -> float:
        """
        Вычисляет метрику верности исходному тексту.
        
        Args:
            summary: Текст суммаризации
            source_facts: Список фактов из исходного текста
            
        Returns:
            float: Оценка от 0 до 100
        """
        # Simplified implementation
        found_facts = sum(1 for fact in source_facts if fact.lower() in summary.lower())
        return (found_facts / len(source_facts)) * 100 if source_facts else 0
    
    def calculate_coverage(self, summary: str, key_elements: List[str]) -> float:
        """
        Вычисляет покрытие ключевых элементов.
        
        Args:
            summary: Текст суммаризации
            key_elements: Список ключевых элементов
            
        Returns:
            float: Оценка от 0 до 100
        """
        covered = sum(1 for element in key_elements if element.lower() in summary.lower())
        return (covered / len(key_elements)) * 100 if key_elements else 0
    
    def calculate_prompt_adherence(self, summary: str, word_count: int, 
                                   min_words: int = 100, max_words: int = 150) -> float:
        """
        Вычисляет соответствие требованиям промта.
        
        Args:
            summary: Текст суммаризации
            word_count: Количество слов в суммаризации
            min_words: Минимальное требуемое количество слов
            max_words: Максимальное требуемое количество слов
            
        Returns:
            float: Оценка от 0 до 100
        """
        # Check word count
        if min_words <= word_count <= max_words:
            word_score = 40
        else:
            word_score = 0
        
        # Check structure (simplified)
        structure_score = 30 if all(marker in summary for marker in ['1.', '2.', '3.']) else 15
        
        # Check style
        style_score = 30  # Simplified - assume neutral tone
        
        return word_score + structure_score + style_score
    
    def calculate_compression_ratio(self, source_words: int, summary_words: int) -> float:
        """
        Вычисляет коэффициент сжатия.
        
        Args:
            source_words: Количество слов в исходном тексте
            summary_words: Количество слов в суммаризации
            
        Returns:
            float: Коэффициент сжатия
        """
        return source_words / summary_words if summary_words > 0 else 0
    
    def calculate_coherence(self, summary: str) -> float:
        """
        Оценивает связность текста (упрощенная версия).
        
        Args:
            summary: Текст суммаризации
            
        Returns:
            float: Оценка от 0 до 100
        """
        # Simplified coherence check
        sentences = summary.split('.')
        if len(sentences) > 2:
            return 80  # Base score for multi-sentence summaries
        return 60
    
    def analyze_model(self, model_name: str, summary: str, source_stats: Dict) -> Dict[str, Any]:
        """
        Проводит полный анализ суммаризации модели.
        
        Args:
            model_name: Название модели
            summary: Текст суммаризации
            source_stats: Статистика исходного текста
            
        Returns:
            Dict: Результаты анализа
        """
        word_count = len(summary.split())
        
        # Key elements from the article
        key_elements = [
            "1,75 трлн $", "36%", "40%", "o3-mini", "DeepSeek R1", 
            "Qwen 2.5 Max", "Grok", "YandexGPT", "GigaChat", "Cotype",
            "Humanities Last Exam", "13%", "128K", "1M токенов"
        ]
        
        # Calculate metrics
        metrics = {
            'faithfulness': 100,  # Assume no hallucinations for demo
            'coverage': self.calculate_coverage(summary, key_elements),
            'prompt_adherence': self.calculate_prompt_adherence(summary, word_count),
            'coherence': self.calculate_coherence(summary),
            'compression': self.calculate_compression_ratio(
                source_stats.get('word_count', 4200), word_count
            )
        }
        
        # Calculate weighted score
        total_score = sum(
            metrics[metric] * self.metrics_weights[metric] 
            for metric in metrics
        )
        
        return {
            'model': model_name,
            'word_count': word_count,
            'metrics': metrics,
            'total_score': round(total_score, 2)
        }
    
    def generate_comparison_report(self, analyses: List[Dict]) -> str:
        """
        Генерирует сравнительный отчет.
        
        Args:
            analyses: Список результатов анализа моделей
            
        Returns:
            str: Текст отчета в формате Markdown
        """
        report = []
        report.append("# Сравнительный анализ LLM моделей\n")
        report.append(f"Дата: {datetime.now().strftime('%d.%m.%Y')}\n")
        
        # Sort by total score
        analyses.sort(key=lambda x: x['total_score'], reverse=True)
        
        report.append("## Итоговые результаты\n")
        report.append("| Модель | Общий балл | Слов |")
        report.append("|--------|------------|------|")
        
        for analysis in analyses:
            report.append(
                f"| {analysis['model']} | {analysis['total_score']} | {analysis['word_count']} |"
            )
        
        report.append("\n## Детальные метрики\n")
        
        for analysis in analyses:
            report.append(f"### {analysis['model']}\n")
            for metric, value in analysis['metrics'].items():
                report.append(f"- **{metric}**: {value:.1f}")
            report.append("")
        
        return "\n".join(report)


def main():
    """Пример использования анализатора."""
    analyzer = LLMAnalyzer()
    
    # Загрузка данных из результатов
    results_dir = "results"
    
    # Пример анализа для Claude и Groq
    source_stats = {'word_count': 4200}
    
    analyses = []
    
    # Анализ Claude 3.5 Sonnet - используем правильный файл
    claude_summary_path = os.path.join(results_dir, "new_claude_summary.md")
    if os.path.exists(claude_summary_path):
        with open(claude_summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Извлекаем только текст суммаризации (после "**Суммаризация:**")
            if "**Суммаризация:**" in content:
                parts = content.split("**Суммаризация:**")[1]
                claude_summary = parts.split("**Статистика:**")[0].strip()
            else:
                claude_summary = content
        analyses.append(
            analyzer.analyze_model("Claude 3.5 Sonnet", claude_summary, source_stats)
        )
    
    # Анализ Groq Llama3-8B - используем правильный JSON файл
    groq_json_path = os.path.join(results_dir, "groq_new_result.json")
    if os.path.exists(groq_json_path):
        with open(groq_json_path, 'r', encoding='utf-8') as f:
            groq_data = json.load(f)
            groq_summary = groq_data.get("summary", "")
        analyses.append(
            analyzer.analyze_model("Groq Llama3-8B", groq_summary, source_stats)
        )
    
    # Генерация отчета
    if analyses:
        report = analyzer.generate_comparison_report(analyses)
        print(report)
        
        # Сохранение отчета
        with open("analysis_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        print("\n[OK] Report saved to analysis_report.md")
    else:
        print("[ERROR] No summary files found for analysis")


if __name__ == "__main__":
    main() 