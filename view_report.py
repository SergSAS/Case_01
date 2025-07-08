#!/usr/bin/env python3
"""
Утилита для просмотра статистики отчетов LLM анализа.
Показывает количество строк, слов и символов в файле отчета.
"""

import os
import sys

def display_report_stats():
    """Показывает статистику по финальному отчету."""
    report_path = os.path.join("reports", "FINAL_STRUCTURED_REPORT.md")
    
    if not os.path.exists(report_path):
        print(f"[ERROR] Final report not found at: {report_path}")
        return 1
    
    print(f"[INFO] Displaying statistics for: {report_path}")
    print("-" * 60)
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = len(content.splitlines())
        words = len(content.split())
        chars = len(content)
        
        print(f"  Lines: {lines}")
        print(f"  Words: {words}")
        print(f"  Characters: {chars}")
        print("-" * 60)
        print("[SUCCESS] Statistics displayed.")
        
    except Exception as e:
        print(f"[ERROR] Failed to read and parse report: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(display_report_stats()) 