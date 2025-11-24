"""
Repeatability Analyzer - Determines if a task can be automated with a script

Analyzes LLM exploration results to determine:
- Are steps deterministic?
- Are obstacles predictable?
- Are decisions rule-based or require LLM interpretation?
- Is DOM structure stable?
"""

from typing import List
from .models import (
    ExplorationResult,
    RepeatabilityScore,
    ExecutionStep,
    Obstacle,
    DecisionPoint
)


class RepeatabilityAnalyzer:
    """
    Analyzes task repeatability from LLM exploration
    """
    
    def analyze(self, exploration: ExplorationResult) -> RepeatabilityScore:
        """
        Analyze exploration results to determine repeatability
        
        Args:
            exploration: Results from LLM exploration
            
        Returns:
            RepeatabilityScore with recommendation
        """
        score = 0
        reasoning_parts = []
        
        # 1. Check if steps are deterministic
        deterministic = self.are_steps_deterministic(exploration.journey_log)
        if deterministic:
            score += 3
            reasoning_parts.append("✓ Steps are deterministic and predictable")
        else:
            reasoning_parts.append("✗ Steps vary or require interpretation")
        
        # 2. Check if obstacles are predictable
        predictable_obstacles = self.are_obstacles_predictable(exploration.obstacles)
        if predictable_obstacles:
            score += 2
            reasoning_parts.append("✓ Obstacles are predictable")
        else:
            reasoning_parts.append("✗ Obstacles are unpredictable")
        
        # 3. Check if decisions are rule-based
        rule_based = self.are_decisions_rule_based(exploration.decisions)
        if rule_based:
            score += 2
            reasoning_parts.append("✓ Decisions follow clear rules")
        else:
            score -= 3
            reasoning_parts.append("✗ Decisions require LLM interpretation")
        
        # 4. Check DOM stability (heuristic based on step count)
        stable_dom = self.is_dom_stable(exploration)
        if stable_dom:
            score += 2
            reasoning_parts.append("✓ DOM structure appears stable")
        else:
            reasoning_parts.append("✗ DOM structure may be dynamic")
        
        # 5. Check for dynamic content
        has_dynamic = self.has_dynamic_content(exploration)
        if has_dynamic:
            score -= 2
            reasoning_parts.append("✗ Contains dynamic content")
        else:
            reasoning_parts.append("✓ Content appears static")
        
        # Determine recommendation
        recommendation = self.get_recommendation(score)
        is_repeatable = score >= 5
        confidence = min(abs(score) / 10, 1.0)
        
        return RepeatabilityScore(
            score=score,
            is_repeatable=is_repeatable,
            confidence=confidence,
            recommendation=recommendation,
            reasoning="\n".join(reasoning_parts),
            deterministic_steps=deterministic,
            predictable_obstacles=predictable_obstacles,
            rule_based_decisions=rule_based,
            stable_dom=stable_dom
        )
    
    def are_steps_deterministic(self, journey_log: List[ExecutionStep]) -> bool:
        """
        Check if steps follow a predictable pattern
        
        Heuristics:
        - Same actions in sequence
        - No random/variable elements
        - Clear navigation flow
        """
        if len(journey_log) == 0:
            return False
        
        # Check for variety in actions (more variety = less deterministic)
        action_types = [step.action for step in journey_log]
        unique_actions = set(action_types)
        
        # If too many different action types, likely not deterministic
        if len(unique_actions) > len(action_types) * 0.7:
            return False
        
        # Check for clear patterns (navigate → fill → click → extract)
        common_patterns = ['navigate', 'click', 'type', 'extract']
        has_pattern = any(action in action_types for action in common_patterns)
        
        return has_pattern
    
    def are_obstacles_predictable(self, obstacles: List[Obstacle]) -> bool:
        """
        Check if obstacles are predictable and handleable
        
        Predictable obstacles:
        - Cookie banners (always appear)
        - Modals (consistent)
        - Ads (can be blocked)
        
        Unpredictable:
        - CAPTCHAs
        - Random redirects
        """
        if len(obstacles) == 0:
            return True  # No obstacles = predictable
        
        # Check if all obstacles have high likelihood
        predictable = all(obs.likelihood > 0.7 for obs in obstacles)
        
        # Check for unpredictable obstacle types
        unpredictable_types = ['captcha', 'random_redirect', 'bot_detection']
        has_unpredictable = any(
            obs.type in unpredictable_types for obs in obstacles
        )
        
        return predictable and not has_unpredictable
    
    def are_decisions_rule_based(self, decisions: List[DecisionPoint]) -> bool:
        """
        Check if decisions can be codified as rules
        
        Rule-based decisions:
        - "Click the first result"
        - "Select option with lowest price"
        - "Fill form with provided data"
        
        LLM-required decisions:
        - "Choose the most relevant article"
        - "Determine if content is trustworthy"
        - "Summarize the main points"
        """
        if len(decisions) == 0:
            return True  # No decisions = rule-based
        
        # Heuristic: if there are many decisions, likely requires LLM
        if len(decisions) > 5:
            return False
        
        # Check for keywords indicating interpretation needed
        interpretation_keywords = [
            'relevant', 'best', 'most', 'summarize', 'analyze',
            'determine', 'evaluate', 'assess', 'judge'
        ]
        
        requires_interpretation = any(
            any(keyword in decision.question.lower() for keyword in interpretation_keywords)
            for decision in decisions
        )
        
        return not requires_interpretation
    
    def is_dom_stable(self, exploration: ExplorationResult) -> bool:
        """
        Check if DOM structure is stable
        
        Heuristics:
        - Consistent selectors
        - No dynamic IDs
        - Predictable structure
        """
        # Simple heuristic: if task completed successfully with reasonable steps
        if exploration.success and len(exploration.journey_log) < 30:
            return True
        
        return False
    
    def has_dynamic_content(self, exploration: ExplorationResult) -> bool:
        """
        Check if page has dynamic content requiring interpretation
        
        Indicators:
        - Many different actions
        - Long execution time
        - Many decision points
        """
        has_many_steps = len(exploration.journey_log) > 20
        has_many_decisions = len(exploration.decisions) > 3
        
        return has_many_steps or has_many_decisions
    
    def get_recommendation(self, score: int) -> str:
        """
        Get execution recommendation based on score
        
        Args:
            score: Repeatability score
            
        Returns:
            'SCRIPT', 'HYBRID', or 'BROWSER_USE'
        """
        if score >= 7:
            return "SCRIPT"  # Highly repeatable - generate script
        elif score >= 3:
            return "HYBRID"  # Partially repeatable - use hybrid approach
        else:
            return "BROWSER_USE"  # Not repeatable - use browser-use
