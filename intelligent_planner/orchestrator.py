"""
Main Orchestrator - Coordinates all components of intelligent browser automation

Flow:
1. LLM explores task → 2. Analyze repeatability → 3. Execute (script or browser-use)
"""

import asyncio
import os
import subprocess
import uuid
from typing import Optional
import logging

from .llm_explorer import LLMExplorer
from .repeatability_analyzer import RepeatabilityAnalyzer
from .script_generator import ScriptGenerator
from .browser_use_executor import BrowserUseExecutor
from .models import ExecutionResult

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptLibrary:
    """Manages saved scripts"""
    
    def __init__(self, library_path: str = "generated_scripts"):
        self.library_path = library_path
        os.makedirs(library_path, exist_ok=True)
    
    def find(self, url: str, task: str) -> Optional[str]:
        """Find existing script for URL/task combination"""
        # Simple hash-based lookup
        script_id = self._generate_id(url, task)
        script_path = os.path.join(self.library_path, f"{script_id}.py")
        
        if os.path.exists(script_path):
            with open(script_path, 'r') as f:
                return f.read()
        return None
    
    def save(self, url: str, task: str, code: str) -> str:
        """Save script to library"""
        script_id = self._generate_id(url, task)
        script_path = os.path.join(self.library_path, f"{script_id}.py")
        
        with open(script_path, 'w') as f:
            f.write(code)
        
        logger.info(f"💾 Script saved to {script_path}")
        return script_path
    
    def _generate_id(self, url: str, task: str) -> str:
        """Generate unique ID for URL/task combination"""
        import hashlib
        combined = f"{url}:{task}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]


class IntelligentBrowserAutomation:
    """
    Main orchestrator for intelligent browser automation
    """
    
    def __init__(self, llm_provider: str = "browser-use"):
        """
        Initialize the automation system
        
        Args:
            llm_provider: 'browser-use', 'gpt4', 'gemini', or 'grok'
        """
        self.llm_explorer = LLMExplorer(llm_provider=llm_provider)
        self.repeatability_analyzer = RepeatabilityAnalyzer()
        self.script_generator = ScriptGenerator(framework="playwright")
        self.browser_use_executor = BrowserUseExecutor()
        self.script_library = ScriptLibrary()
    
    async def execute(self, url: str, task: str) -> ExecutionResult:
        """
        Execute a browser automation task
        
        Args:
            url: Starting URL
            task: Task description
            
        Returns:
            ExecutionResult with method used and results
        """
        logger.info("=" * 60)
        logger.info(f"🎯 Task: {task}")
        logger.info(f"🌐 URL: {url}")
        logger.info("=" * 60)
        
        # Check if we have a script for this task
        existing_script = self.script_library.find(url, task)
        if existing_script:
            logger.info("📚 Found existing script in library")
            try:
                result = await self._execute_script(existing_script)
                logger.info("✅ Script executed successfully!")
                return result
            except Exception as e:
                logger.warning(f"⚠️  Script failed: {e}")
                logger.info("🔄 Falling back to exploration...")
        
        # Phase 1: LLM Exploration
        logger.info("🔍 Phase 1: Exploring task with LLM...")
        exploration = await self.llm_explorer.explore_task(url, task)
        
        if not exploration.success:
            logger.error(f"❌ Exploration failed: {exploration.error}")
            return ExecutionResult(
                success=False,
                method="EXPLORATION_FAILED",
                result=None,
                error=exploration.error
            )
        
        logger.info(f"✅ Exploration completed ({len(exploration.journey_log)} steps)")
        
        # Phase 2: Repeatability Analysis
        logger.info("📊 Phase 2: Analyzing repeatability...")
        analysis = self.repeatability_analyzer.analyze(exploration)
        
        logger.info(f"📈 Repeatability score: {analysis.score}")
        logger.info(f"💡 Recommendation: {analysis.recommendation}")
        logger.info(f"🎯 Confidence: {analysis.confidence:.0%}")
        logger.info(f"\n{analysis.reasoning}")
        
        # Phase 3: Execute based on recommendation
        if analysis.recommendation == "SCRIPT":
            return await self._execute_with_script(exploration, url, task)
        
        elif analysis.recommendation == "BROWSER_USE":
            return await self._execute_with_browser_use(url, task, exploration)
        
        else:  # HYBRID
            return await self._execute_hybrid(exploration, url, task)
    
    async def _execute_with_script(
        self,
        exploration,
        url: str,
        task: str
    ) -> ExecutionResult:
        """Execute using generated script"""
        logger.info("⚙️  Phase 3: Generating Python script...")
        
        # Generate script
        script = await self.script_generator.generate_from_exploration(
            exploration, url, task
        )
        
        # Save to temporary file for testing
        script_path = f"generated_scripts/test_{uuid.uuid4().hex[:8]}.py"
        os.makedirs("generated_scripts", exist_ok=True)
        with open(script_path, 'w') as f:
            f.write(script.code)
        
        logger.info(f"📝 Script generated: {script_path}")
        logger.info("🧪 Testing script...")
        
        # Test script
        try:
            result = await self._execute_script(script.code)
            
            # Save to library if successful
            saved_path = self.script_library.save(url, task, script.code)
            logger.info(f"✅ Script works! Saved to library: {saved_path}")
            
            return ExecutionResult(
                success=True,
                method="SCRIPT",
                result=result,
                script_path=saved_path
            )
        
        except Exception as e:
            logger.warning(f"⚠️  Script test failed: {e}")
            logger.info("🔄 Falling back to browser-use...")
            return await self._execute_with_browser_use(url, task, exploration)
    
    async def _execute_with_browser_use(
        self,
        url: str,
        task: str,
        exploration=None
    ) -> ExecutionResult:
        """Execute using browser-use agent"""
        logger.info("🤖 Phase 3: Using browser-use for execution...")
        
        result = await self.browser_use_executor.execute_non_repeatable(
            url, task, exploration
        )
        
        if result.success:
            logger.info("✅ Browser-use execution successful!")
        else:
            logger.error(f"❌ Browser-use execution failed: {result.error}")
        
        return result
    
    async def _execute_hybrid(
        self,
        exploration,
        url: str,
        task: str
    ) -> ExecutionResult:
        """Execute using hybrid approach"""
        logger.info("🔄 Phase 3: Using hybrid approach...")
        
        # Try script first
        try:
            return await self._execute_with_script(exploration, url, task)
        except Exception as e:
            logger.info(f"Script failed: {e}, using browser-use")
            return await self._execute_with_browser_use(url, task, exploration)
    
    async def _execute_script(self, script_code: str) -> str:
        """Execute a Python script"""
        # Save to temp file
        temp_path = f"/tmp/script_{uuid.uuid4().hex[:8]}.py"
        with open(temp_path, 'w') as f:
            f.write(script_code)
        
        # Execute
        result = subprocess.run(
            ['python', temp_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            raise Exception(f"Script failed: {result.stderr}")
        
        return result.stdout


# Example usage
async def main():
    """Example usage of IntelligentBrowserAutomation"""
    
    # Initialize
    automation = IntelligentBrowserAutomation(llm_provider="browser-use")
    
    # Example 1: Repeatable task
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Repeatable Task")
    print("=" * 60)
    
    result1 = await automation.execute(
        url="https://news.ycombinator.com",
        task="Find the title of the top post"
    )
    
    print(f"\n✅ Result: {result1.result}")
    print(f"📊 Method: {result1.method}")
    
    # Example 2: Run same task again (should use script)
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Re-run Same Task (Should Use Script)")
    print("=" * 60)
    
    result2 = await automation.execute(
        url="https://news.ycombinator.com",
        task="Find the title of the top post"
    )
    
    print(f"\n✅ Result: {result2.result}")
    print(f"📊 Method: {result2.method}")


if __name__ == "__main__":
    asyncio.run(main())
