"""
LLM Explorer - Uses powerful LLMs with web browsing to explore and complete tasks

Supports:
- GPT-4 with browsing (OpenAI API)
- Grok with web access (X.AI API)  
- Gemini with search/browse (Google AI API)
"""

import asyncio
import json
from typing import Optional
from datetime import datetime

from .models import (
    ExplorationResult,
    ExecutionStep,
    Obstacle,
    DecisionPoint
)


class LLMExplorer:
    """
    Uses LLM with web browsing capability to explore tasks
    """
    
    def __init__(self, llm_provider: str = "browser-use"):
        """
        Initialize LLM Explorer
        
        Args:
            llm_provider: 'gpt4', 'grok', 'gemini', or 'browser-use'
        """
        self.llm_provider = llm_provider
        self.llm = self._initialize_llm(llm_provider)
    
    def _initialize_llm(self, provider: str):
        """Initialize the appropriate LLM"""
        if provider == "browser-use":
            # Use browser-use itself for exploration
            from browser_use import Agent, Browser, ChatBrowserUse
            return {
                'type': 'browser-use',
                'browser': Browser(headless=True),
                'llm': ChatBrowserUse()
            }
        elif provider == "gpt4":
            # GPT-4 with browsing capability
            from openai import AsyncOpenAI
            return {
                'type': 'gpt4',
                'client': AsyncOpenAI()
            }
        elif provider == "gemini":
            # Gemini with search/browse
            import google.generativeai as genai
            return {
                'type': 'gemini',
                'client': genai
            }
        elif provider == "grok":
            # Grok with web access
            return {
                'type': 'grok',
                'client': None  # TODO: Add Grok client
            }
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    async def explore_task(self, url: str, task: str) -> ExplorationResult:
        """
        Use LLM to explore and complete the task
        
        Args:
            url: Starting URL
            task: Task description
            
        Returns:
            ExplorationResult with journey log, obstacles, and decisions
        """
        print(f"🔍 Exploring task with {self.llm_provider}...")
        
        if self.llm['type'] == 'browser-use':
            return await self._explore_with_browser_use(url, task)
        elif self.llm['type'] == 'gpt4':
            return await self._explore_with_gpt4(url, task)
        elif self.llm['type'] == 'gemini':
            return await self._explore_with_gemini(url, task)
        else:
            raise NotImplementedError(f"Explorer for {self.llm['type']} not implemented")
    
    async def _explore_with_browser_use(self, url: str, task: str) -> ExplorationResult:
        """
        Explore using browser-use agent
        """
        from browser_use import Agent
        
        # Enhanced task with exploration instructions
        exploration_task = f"""
        Complete this task: {task}
        
        Starting URL: {url}
        
        IMPORTANT: As you work, document:
        1. Every action you take (clicks, typing, navigation, scrolling)
        2. Any obstacles encountered (modals, ads, redirects, cookie banners)
        3. Decision points (why you chose specific actions)
        4. Page structure patterns you notice
        
        Complete the task fully and provide detailed results.
        """
        
        agent = Agent(
            task=exploration_task,
            browser=self.llm['browser'],
            llm=self.llm['llm'],
            use_vision=True,  # Use screenshots for better understanding
            max_actions_per_step=10
        )
        
        try:
            history = await agent.run(max_steps=50)
            
            # Parse history into exploration result
            journey_log = []
            obstacles = []
            decisions = []
            
            # Extract steps from history
            for i, action in enumerate(history.model_actions()):
                step = ExecutionStep(
                    step_number=i + 1,
                    action=action.get('action', 'unknown'),
                    target=action.get('target'),
                    value=action.get('value'),
                    timestamp=datetime.now().isoformat()
                )
                journey_log.append(step)
            
            # Analyze for obstacles (simple heuristic)
            action_names = history.action_names()
            if any('click' in a.lower() and 'accept' in str(a).lower() for a in action_names):
                obstacles.append(Obstacle(
                    type='cookie_banner',
                    likelihood=0.9,
                    handling_strategy='click_accept',
                    detected_at_step=1
                ))
            
            # Calculate repeatability score
            repeatability_score = self._calculate_repeatability(journey_log, obstacles, decisions)
            
            return ExplorationResult(
                success=history.is_successful(),
                journey_log=journey_log,
                obstacles=obstacles,
                decisions=decisions,
                final_result=str(history.final_result()),
                repeatability_score=repeatability_score
            )
            
        except Exception as e:
            return ExplorationResult(
                success=False,
                journey_log=[],
                obstacles=[],
                decisions=[],
                error=str(e)
            )
    
    async def _explore_with_gpt4(self, url: str, task: str) -> ExplorationResult:
        """
        Explore using GPT-4 with browsing
        
        Note: This requires GPT-4 with browsing capability (ChatGPT Plus feature)
        For now, we'll use browser-use as a fallback
        """
        # TODO: Implement GPT-4 browsing integration
        print("⚠️ GPT-4 browsing not yet implemented, using browser-use")
        return await self._explore_with_browser_use(url, task)
    
    async def _explore_with_gemini(self, url: str, task: str) -> ExplorationResult:
        """
        Explore using Gemini with search/browse
        """
        # TODO: Implement Gemini browsing integration
        print("⚠️ Gemini browsing not yet implemented, using browser-use")
        return await self._explore_with_browser_use(url, task)
    
    def _calculate_repeatability(
        self,
        journey_log: list,
        obstacles: list,
        decisions: list
    ) -> float:
        """
        Calculate initial repeatability score based on exploration
        
        Returns:
            Score from 0.0 (not repeatable) to 1.0 (highly repeatable)
        """
        score = 0.5  # Start neutral
        
        # More steps = potentially more complex = less repeatable
        if len(journey_log) > 20:
            score -= 0.1
        elif len(journey_log) < 10:
            score += 0.1
        
        # Predictable obstacles = more repeatable
        if len(obstacles) > 0 and all(o.likelihood > 0.7 for o in obstacles):
            score += 0.2
        
        # Many decisions = less repeatable
        if len(decisions) > 5:
            score -= 0.2
        
        return max(0.0, min(1.0, score))


# Example usage
async def example():
    """Example of using LLM Explorer"""
    explorer = LLMExplorer(llm_provider="browser-use")
    
    result = await explorer.explore_task(
        url="https://news.ycombinator.com",
        task="Find the top post and extract its title"
    )
    
    print(f"Success: {result.success}")
    print(f"Steps taken: {len(result.journey_log)}")
    print(f"Obstacles found: {len(result.obstacles)}")
    print(f"Repeatability score: {result.repeatability_score}")
    print(f"Result: {result.final_result}")


if __name__ == "__main__":
    asyncio.run(example())
