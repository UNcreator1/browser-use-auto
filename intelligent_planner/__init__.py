"""
Intelligent Browser Automation System

A 100% reliable browser automation system that:
1. Explores tasks using powerful LLMs (GPT-4/Grok/Gemini) with web browsing
2. Analyzes if tasks are repeatable → generate Python script, or non-repeatable → use browser-use
3. Executes using optimal approach: generated scripts (fast, cheap) or browser-use (flexible, adaptive)
4. Learns from each execution to improve future performance
"""

from .orchestrator import IntelligentBrowserAutomation
from .models import (
    ExplorationResult,
    RepeatabilityScore,
    ExecutionResult,
    TaskType
)

__all__ = [
    'IntelligentBrowserAutomation',
    'ExplorationResult',
    'RepeatabilityScore',
    'ExecutionResult',
    'TaskType'
]

__version__ = '0.1.0'
