"""
Script Generator - Converts LLM exploration into executable Python scripts

Generates Playwright/Selenium scripts from exploration journey
"""

import uuid
from typing import List
from datetime import datetime

from .models import (
    ExplorationResult,
    GeneratedScript,
    ExecutionStep,
    Obstacle
)


class ScriptGenerator:
    """
    Generates Python scripts from LLM exploration
    """
    
    def __init__(self, framework: str = "playwright"):
        """
        Initialize script generator
        
        Args:
            framework: 'playwright' or 'selenium'
        """
        self.framework = framework
    
    async def generate_from_exploration(
        self,
        exploration: ExplorationResult,
        url: str,
        task: str
    ) -> GeneratedScript:
        """
        Generate executable script from exploration
        
        Args:
            exploration: LLM exploration results
            url: Starting URL
            task: Task description
            
        Returns:
            GeneratedScript with code
        """
        if self.framework == "playwright":
            code = self._generate_playwright_script(exploration, url, task)
            dependencies = ["playwright"]
        else:
            code = self._generate_selenium_script(exploration, url, task)
            dependencies = ["selenium"]
        
        return GeneratedScript(
            code=code,
            language="python",
            dependencies=dependencies
        )
    
    def _generate_playwright_script(
        self,
        exploration: ExplorationResult,
        url: str,
        task: str
    ) -> str:
        """Generate Playwright script"""
        
        # Generate obstacle handlers
        obstacle_handlers = self._generate_obstacle_handlers(exploration.obstacles)
        
        # Generate main steps
        main_steps = self._generate_main_steps(exploration.journey_log)
        
        # Generate extraction logic
        extract_logic = self._generate_extract_logic(exploration)
        
        script = f'''"""
Auto-generated script from LLM exploration
Task: {task}
URL: {url}
Generated: {datetime.now().isoformat()}
Framework: Playwright
"""

import asyncio
from playwright.async_api import async_playwright


async def automated_task():
    """Execute the automated task"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("🚀 Starting automation...")
            
            # Step 1: Navigate to URL
            print(f"📍 Navigating to {{url}}")
            await page.goto('{url}')
            await page.wait_for_load_state('networkidle')
            
{obstacle_handlers}
            
{main_steps}
            
{extract_logic}
            
            print("✅ Task completed successfully!")
            return result
            
        except Exception as e:
            print(f"❌ Error: {{e}}")
            raise
        finally:
            await browser.close()


if __name__ == "__main__":
    result = asyncio.run(automated_task())
    print(f"\\n📊 Result: {{result}}")
'''
        return script
    
    def _generate_obstacle_handlers(self, obstacles: List[Obstacle]) -> str:
        """Generate code to handle obstacles"""
        if not obstacles:
            return "            # No obstacles detected"
        
        handlers = []
        handlers.append("            # Handle common obstacles")
        
        for obstacle in obstacles:
            if obstacle.type == 'cookie_banner':
                handlers.append('''
            # Handle cookie banner
            try:
                print("🍪 Handling cookie banner...")
                await page.click('button:has-text("Accept"), button:has-text("Đồng ý"), button:has-text("同意")', timeout=3000)
                await page.wait_for_timeout(500)
            except:
                pass  # Continue if not found
''')
            elif obstacle.type == 'modal':
                handlers.append('''
            # Handle modal
            try:
                print("📋 Closing modal...")
                await page.click('button:has-text("Close"), button.close, .modal-close', timeout=2000)
                await page.wait_for_timeout(500)
            except:
                pass
''')
            elif obstacle.type == 'ad':
                handlers.append('''
            # Handle ads
            try:
                print("🚫 Blocking ads...")
                await page.evaluate("document.querySelectorAll('.ad, .advertisement').forEach(el => el.remove())")
            except:
                pass
''')
        
        return "\n".join(handlers)
    
    def _generate_main_steps(self, journey_log: List[ExecutionStep]) -> str:
        """Generate main execution steps"""
        if not journey_log:
            return "            # No steps recorded"
        
        steps = []
        steps.append("            # Main execution steps")
        
        for i, step in enumerate(journey_log, 1):
            if step.action == 'click':
                steps.append(f'''
            # Step {i}: Click
            print("🖱️  Clicking element...")
            await page.click('{step.target or "button"}')
            await page.wait_for_timeout(1000)
''')
            elif step.action in ['type', 'fill']:
                steps.append(f'''
            # Step {i}: Fill input
            print("⌨️  Typing text...")
            await page.fill('{step.target or "input"}', '{step.value or ""}')
''')
            elif step.action == 'navigate':
                steps.append(f'''
            # Step {i}: Navigate
            print("🔗 Navigating...")
            await page.goto('{step.value or step.target}')
            await page.wait_for_load_state('networkidle')
''')
            elif step.action == 'scroll':
                steps.append('''
            # Step {i}: Scroll
            print("📜 Scrolling...")
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(500)
''')
        
        return "\n".join(steps)
    
    def _generate_extract_logic(self, exploration: ExplorationResult) -> str:
        """Generate data extraction logic"""
        return '''
            # Extract results
            print("📊 Extracting data...")
            result = {
                'success': True,
                'data': await page.evaluate('document.body.innerText'),
                'url': page.url
            }
'''
    
    def _generate_selenium_script(
        self,
        exploration: ExplorationResult,
        url: str,
        task: str
    ) -> str:
        """Generate Selenium script"""
        # TODO: Implement Selenium script generation
        return f'''"""
Selenium script generation not yet implemented
Use Playwright instead
"""
'''


# Example usage
async def example():
    """Example of script generation"""
    from .llm_explorer import LLMExplorer
    
    # First, explore the task
    explorer = LLMExplorer()
    exploration = await explorer.explore_task(
        url="https://example.com",
        task="Fill out contact form"
    )
    
    # Generate script
    generator = ScriptGenerator(framework="playwright")
    script = await generator.generate_from_exploration(
        exploration,
        url="https://example.com",
        task="Fill out contact form"
    )
    
    print("Generated Script:")
    print("=" * 60)
    print(script.code)


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
