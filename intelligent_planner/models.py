"""
Data models for intelligent browser automation system
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Type of task based on repeatability"""
    REPEATABLE = "REPEATABLE"
    NON_REPEATABLE = "NON_REPEATABLE"
    HYBRID = "HYBRID"


class ExecutionStep(BaseModel):
    """Single step in task execution"""
    step_number: int
    action: str  # 'navigate', 'click', 'type', 'extract', 'scroll', etc.
    target: Optional[str] = None
    value: Optional[str] = None
    timestamp: Optional[str] = None
    screenshot: Optional[str] = None


class Obstacle(BaseModel):
    """Detected obstacle during exploration"""
    type: str  # 'modal', 'ad', 'redirect', 'captcha', 'cookie_banner', 'scroll'
    likelihood: float = Field(ge=0.0, le=1.0)
    handling_strategy: str
    detected_at_step: Optional[int] = None


class DecisionPoint(BaseModel):
    """Point where LLM made a decision"""
    step_number: int
    question: str
    decision: str
    reasoning: str
    alternatives: List[str] = []


class ExplorationResult(BaseModel):
    """Result from LLM exploration"""
    success: bool
    journey_log: List[ExecutionStep]
    obstacles: List[Obstacle]
    decisions: List[DecisionPoint]
    page_structure: Optional[Dict[str, Any]] = None
    final_result: Optional[str] = None
    error: Optional[str] = None
    repeatability_score: Optional[float] = None


class RepeatabilityScore(BaseModel):
    """Analysis of task repeatability"""
    score: int
    is_repeatable: bool
    confidence: float = Field(ge=0.0, le=1.0)
    recommendation: str  # 'SCRIPT', 'BROWSER_USE', 'HYBRID'
    reasoning: str = ""
    deterministic_steps: bool = False
    predictable_obstacles: bool = False
    rule_based_decisions: bool = False
    stable_dom: bool = False


class GeneratedScript(BaseModel):
    """Generated Python script"""
    code: str
    language: str = "python"  # 'python' (Playwright) or 'selenium'
    dependencies: List[str] = []
    test_status: Optional[str] = None
    script_path: Optional[str] = None


class ExecutionResult(BaseModel):
    """Result from task execution"""
    success: bool
    method: str  # 'SCRIPT', 'BROWSER_USE', 'HYBRID'
    result: Any
    steps: Optional[int] = None
    duration: Optional[float] = None
    cost: Optional[float] = None
    error: Optional[str] = None
    script_path: Optional[str] = None
    actions: Optional[List[str]] = None


class TestResult(BaseModel):
    """Result from script testing"""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    duration: Optional[float] = None
