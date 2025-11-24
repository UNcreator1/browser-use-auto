"""
Browser-Use Executor - Executes non-repeatable tasks using browser-use

Uses the accessibility tree → LLM → commands → actions flow
"""

from browser_use import Agent, Browser, ChatBrowserUse

from .models import (
    ExplorationResult,
    ExecutionResult
)


class BrowserUseExecutor:
    """
    Executes tasks using browser-use agent
    """
    
    async def execute_non_repeatable(
        self,
        url: str,
        task: str,
        exploration: ExplorationResult = None
    ) -> ExecutionResult:
        """
        Execute non-repeatable task using browser-use
        
        Args:
            url: Starting URL
            task: Task description
            exploration: Optional exploration results for guidance
            
        Returns:
            ExecutionResult
        """
        # Enhance task with exploration insights if available
        if exploration and exploration.success:
            enhanced_task = self._enhance_task_with_exploration(task, exploration)
        else:
            enhanced_task = task
        
        browser = Browser(headless=True)
        
        agent = Agent(
            task=enhanced_task,
            browser=browser,
            llm=ChatBrowserUse(),
            use_vision=True,  # Use screenshots for better understanding
            max_actions_per_step=10
        )
        
        try:
            history = await agent.run(max_steps=50)
            
            return ExecutionResult(
                success=history.is_successful(),
                method="BROWSER_USE",
                result=history.final_result(),
                steps=history.number_of_steps(),
                duration=history.total_duration_seconds(),
                actions=history.action_names()
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                method="BROWSER_USE",
                result=None,
                error=str(e)
            )
    
    def _enhance_task_with_exploration(
        self,
        task: str,
        exploration: ExplorationResult
    ) -> str:
        """
        Enhance task description with exploration insights
        """
        obstacles_text = ""
        if exploration.obstacles:
            obstacle_types = [obs.type for obs in exploration.obstacles]
            obstacles_text = f"\n\nExpected obstacles: {', '.join(obstacle_types)}"
        
        hints_text = ""
        if len(exploration.journey_log) > 0:
            hints_text = f"\n\nGeneral approach: Complete in ~{len(exploration.journey_log)} steps"
        
        enhanced = f"""{task}{obstacles_text}{hints_text}

Work carefully and handle any obstacles you encounter."""
        
        return enhanced
